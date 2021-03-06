import subprocess
import sys
import re
import time

from . import errors
from . import slack
from . import stream
from . import utils
from .templates import Template


from ruamel.yaml import YAML
yaml=YAML()

import slacker
import io
import copy
import editor
import json

def main():
    try:
        sys.exit(run())
    except errors.SourceDoesNotExistError as e:
        raise()
        sys.stderr.write("Channel, group or user '{}' does not exist".format(e.args[0]))
        sys.exit(1)
    except errors.InvalidSlackToken as e:
        sys.stderr.write("Invalid Slack token: '{}'".format(e.args[0]))
        sys.exit(1)

def run():
    parser = utils.get_parser("""Send, pipe, upload and receive Slack messages from the CLI""")
    group_send = parser.add_argument_group("Send messages")
    group_send.add_argument("-d", "--dst", help="Send message to a Slack channel, group or username")
    group_send.add_argument("-f", "--file", help="Upload file")
    group_send.add_argument("--pre", action="store_true", help="Send as verbatim `message`")
    group_send.add_argument(
        "--run", action="store_true",
        help="Run the message as a shell command and send both the message and the command output"
    )
    group_send.add_argument("messages", nargs="*",
                            help="Messages to send (messages can also be sent from standard input)")

    group_receive = parser.add_argument_group("Receive messages")
    group_receive.add_argument("-s", "--src", action='append',
                               help="Receive messages from a Slack channel, group or username")
    group_receive.add_argument("-l", "--last", type=int,
                               help="Print the last N messages")

    group_dump = parser.add_argument_group("Dump messages")
    group_dump.add_argument("--dump", action='append',
                               help="dump message from a slack 'share this message' URL to STDOUT")

    group_ipython = parser.add_argument_group("IPython")
    group_ipython.add_argument("--ipython", action='store_true',
                               help="Start IPython shell to test API")


    group_edit = parser.add_argument_group("Edit message")
    group_edit.add_argument("--edit", action='append',
                               help="Edit slack message as a YAML file. EDIT is the URL  from the'share this message' context menu. Edit is done using $EDITOR")
    group_edit.add_argument("--create", action='store_true',
                               help="Create new message in the same channel referenced by the EDIT deeplink using $EDITOR. ")
    group_edit.add_argument("--reply", action='store_true',
                               help="Create new (threaded) reply to message refereced by the EDIT deeplink using $EDITOR. ")
    group_edit.add_argument("--user", action='append',
                               help="Send ephemeral message to user in channel referenced by the EDIT deeplink.")
    args = utils.parse_args(parser)

    # Debug command line arguments
    error_message = args_error_message(args)
    if error_message:
        sys.stderr.write(error_message)
        parser.print_help()
        return 1

    # Stream content
    if args.src and args.last is None:
        stream.receive(args.src)
        return 0

    # Print last messages
    if args.src and args.last is not None:
        last_messages(args.src, args.last)
        return 0

    # Send file
    if args.file:
        upload_file(args.dst, args.file)
        return 0


    # Dump messages
    if args.dump :
        for msgurl in args.dump :
            sys.stdout.write("# URL: {msgurl}\n".format(**locals()))
            yaml.dump(fetch_message(msgurl),sys.stdout)
        return 0


    # start IPython

    if args.ipython :
        print("Starting IPython")
        import IPython
        api=slack.client()
        IPython.embed(header="use 'api' as the client")
        return 0

    # edit message

    if args.edit :
        for msgurl in args.edit :
            if args.create :
                create_message(msgurl,reply=args.reply,user=args.user)
            else :
                edit_message(msgurl)
        return 0


    # Pipe content
    if not args.messages:
        pipe(args.dst, pre=args.pre)
        return 0

    # Send messages
    for message in args.messages:
        if args.run:
            run_command(args.dst, message)
        else:
            send_message(args.dst, message, pre=args.pre)
    return 0




# pylint: disable=too-many-return-statements
def args_error_message(args):
    if args.dst and args.src:
        return "Incompatible arguments: --src and --dst\n"
    if not args.dst and not args.src and not args.dump and not args.ipython and not args.edit :
        return "Invalid arguments: one of --src or --dst or --edit or --dump or --ipython must be specified\n"
    if args.dst and args.last:
        return "Incompatible arguments: --dst and --last\n"
    if args.src and args.file:
        return "Incompatible arguments: --src and --file\n"
    if args.file and args.messages:
        return "Incompatible arguments: `messages` and --file\n"

    return None

######### Receive

def last_messages(sources, count):
    for source in sources:
        utils.search_messages(source, count=count)

######### Send

def pipe(destination, pre=False):
    destination_id = utils.get_source_id(destination)
    for line in sys.stdin:
        line = line.strip()
        if line:
            slack.post_message(destination_id, line, pre=pre)

def run_command(destination, command):
    destination_id = utils.get_source_id(destination)
    command_result = subprocess.check_output(command, shell=True)
    message = "$ " + command + "\n" + command_result.decode("utf-8")
    slack.post_message(destination_id, message, pre=True)

def send_message(destination, message, pre=False):
    destination_id = utils.get_source_id(destination)
    slack.post_message(destination_id, message, pre=pre)

def upload_file(destination, path):
    destination_id = utils.get_source_id(destination)
    utils.upload_file(path, destination_id)

########## Dump

def fetch_message(url) :
    parts=re.search(r"/(?P<channel>[^/]+)/p(?P<seconds>[0-9]+)(?P<nanoseconds>[0-9]{6})$",url)
    client=slack.client()
    if parts :
        m=parts.groupdict()
        ts="{seconds}.{nanoseconds}".format(**m)
        try :
            ctype="channel"
            result=client.channels.history(channel=m["channel"],latest=ts,oldest=ts,inclusive=True)
        except slacker.Error :
            ctype="conversation"
            result=client.channels.get('conversations.history',
                        params={
                            'channel': m["channel"],
                            'latest': ts,
                            'oldest': ts,
                            'inclusive': 1
                        })
    else :
        parts=re.search(r"/(?P<channel>[^/]+)/p(?P<seconds>[0-9]+)(?P<nanoseconds>[0-9]{6})\?thread_ts=(?P<thread_ts>[0-9\.]+)",url)
        if parts :
            m=parts.groupdict()
            ts="{seconds}.{nanoseconds}".format(**m)
            try :
                ctype="conversation.reply"
                result=client.channels.get("conversations.replies",params=dict(channel=m["channel"],ts=m["thread_ts"]))
            except slacker.Error as e:
                print("error: ",e)
                ctype="channel.reply"
                result=client.channels.get("channels.replies",params=dict(channel=m["channel"],thread_ts=m["thread_ts"]))
            result.body["messages"]=[ a for a in result.body["messages"] if a["ts"] == ts]
        else :
            raise ValueError("{url} was not in the expected format. Example: https://next-lab.slack.com/archives/C8WFT1MHT/p1516995098000460 or https://next-lab.slack.com/archives/C8WFT1MHT/p1517846831000338?thread_ts=1517846796.000121&cid=C8WFT1MHT ".format(**locals()))
    try :
        return dict(ctype=ctype, channel=m["channel"],message=result.body["messages"][0])
    except Exception as e :
        raise ValueError("No message found for url {url}".format(**locals()))

########## Edit
import logging

logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.ERROR)

def yaml_from_string(content) :
    buf = io.StringIO()
    buf.write(content.decode("utf-8"))
    buf.seek(0)
    return yaml.load(buf)

def edit_valid_yaml(content) :
    success=False
    while not success :
        result=editor.edit(contents=content)
        if result == content :
            print("Unchanged - aborting")
            success=True
            result=False
            return result
        try :
            yaml_from_string(result)
        except Exception as e :
            logging.exception(e)
            print(f"Retry: {e}")
            time.sleep(2)
            content=result
        else :
            success=True
    return result


    result=yaml.load(editor.edit(contents=Template.edit_message.render(message).encode("utf-8")))


def edit_message(url) :
    message = fetch_message(url)
    import editor
    if "attachments" in message["message"] :
        atts = []
        for att in message["message"]["attachments"] :
            if "id" in att :
                del att["id"]
            atts.append(copy.deepcopy(att))
        buf = io.StringIO()
        yaml.dump({"attachments" : atts},buf)
        buf.seek(0)
        message["message"]["attachments_yaml"]=buf.read()
    result=edit_valid_yaml(Template.edit_message.render(message).encode("utf-8"))
    if result == False :
        return
    result=yaml_from_string(result)
    client=slack.client()
    parse=result.get('parse','full')
    if "attachments" in result :
        response=client.chat.update(result["channel"],result["ts"],result["text"],parse=parse,attachments=result["attachments"],link_names=1)
    else :
        response=client.chat.update(result["channel"],result["ts"],result["text"],parse=parse,link_names=1)
    # print(client.get_permalink(response.body["channel"],response.body["ts"]))
    #import IPython
    #IPython.embed(header="response?")

def create_message(url,reply=False,user=False) :
    message = fetch_message(url)
    if reply :
        result=edit_valid_yaml(Template.create_reply.render(message).encode("utf-8"))
    else :
        result=edit_valid_yaml(Template.create_message.render(message).encode("utf-8"))
    if result == False :
        return
    result=yaml_from_string(result)
    client=slack.client()
    param=dict()
    for p in ('text','username','icon_url','icon_emoji','attachments','as_user') :
        if p in result :
            param[p]=result[p]
    if reply and "thread_ts" in result :
        param["thread_ts"]=result["thread_ts"]
    if user :
        for p in ('username', 'icon_emoji','icon_url') :
            if p in param :
                del param[p]
        response=client.chat.post_ephemeral(result["channel"],user=user, **param)
    else :
        response=client.chat.post_message(result["channel"],**param)
    # print(client.chat.get_permalink(response.body["channel"],response.body["ts"]))
        link=r=client.chat.get('chat.getPermalink',params=dict(channel=response.body["channel"],message_ts=response.body["ts"]))
        print(link.body["permalink"])
