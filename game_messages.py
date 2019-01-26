import tcod as tcod

import textwrap


class Message:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color

    def __repr__(self):
        return f'Message: text = {self.text}, color = {self.color}'


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # Split the message if necessary, among lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If buffer is full, remove first line
            if len(self.messages) == self.height:
                del self.messages[0]

            # add the new line as a message object, with the text and the color
            self.messages.append(Message(line, message.color))

    def __repr__(self):
        return f'MessageLog: messages = {self.messages}, x = {self.x}, width = {self.width}, height = {self.height}'
