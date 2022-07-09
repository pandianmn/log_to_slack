from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import traceback
from logging import (
    Handler,
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    FATAL,
    DEBUG,
    NOTSET,
    Formatter,
)

import six

ERROR_COLOR = "#FF0000"
WARNING_COLOR = "#FFCC00"
INFO_COLOR = "#439FE0"

COLORS = {
    CRITICAL: ERROR_COLOR,
    FATAL: ERROR_COLOR,
    ERROR: ERROR_COLOR,
    WARNING: WARNING_COLOR,
    INFO: INFO_COLOR,
    DEBUG: INFO_COLOR,
    NOTSET: INFO_COLOR,
}

DEFAULT_EMOJI = ":heavy_exclamation_mark:"


class NoStacktraceFormatter(Formatter):
    """
    By default the stacktrace will be formatted as part of the message.
    Since we want the stacktrace to be in the attachment of the Slack message,
     we need a custom formatter to leave it out of the message
    """

    def formatException(self, ei):
        return None

    def format(self, record):
        # Work-around for https://bugs.python.org/issue29056
        saved_exc_text = record.exc_text
        record.exc_text = None
        try:
            return super(NoStacktraceFormatter, self).format(record)
        finally:
            record.exc_text = saved_exc_text


class SlackLogHandler(Handler):
    def __init__(
        self,
        slack_token,
        channel,
        stack_trace=True,
        username="Python logger",
        icon_url=None,
        icon_emoji=None,
        fail_silent=False,
    ):
        Handler.__init__(self)
        self.formatter = NoStacktraceFormatter()

        self.stack_trace = stack_trace
        self.fail_silent = fail_silent

        self.client = WebClient(token=slack_token)

        self.username = username
        self.icon_url = icon_url
        self.icon_emoji = icon_emoji if (icon_emoji or icon_url) else DEFAULT_EMOJI
        self.channel = channel

    def build_msg(self, record):
        return six.text_type(self.format(record))

    def build_trace(self, record, fallback):
        trace = {
            "fallback": fallback,
            "color": COLORS.get(record.levelno, INFO_COLOR),
        }

        if record.exc_info:
            text = "\n".join(traceback.format_exception(*record.exc_info))
            trace["text"] = f"```{text}```"
        return trace

    def emit(self, record):
        message = self.build_msg(record)
        if self.stack_trace:
            trace = self.build_trace(record, fallback=message)
            attachments = [trace]
        else:
            attachments = None

        try:
            self.client.chat_postMessage(
                text=message,
                channel=self.channel,
                username=self.username,
                icon_url=self.icon_url,
                icon_emoji=self.icon_emoji,
                attachments=attachments,
            )
        except SlackApiError as e:
            if self.fail_silent:
                pass
            else:
                raise e
