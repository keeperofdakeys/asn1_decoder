from collections import deque

class LexError(Exception):
    pass

class Lexer():
    def __init__(self):
        self.white_space = []
        self.comments = []
        self.quotes = []
        self.separators = []

        self.source = None
        self.offset = 0
        self.length = 0

    def _handle_comment(self, new_offset, comment_func):
        return comment_func

    def tokens(self):
        escaped = False
        quoted = False
        quote_char = None

        # Store a deque of char_lists
        # Use list of chars for append performance
        char_lists = deque()
        char_lists.append([])
        next_offset = 0

        while next_offset < self.length:
            print char_lists
            next_char = self.source[next_offset]
            cur_offset = next_offset
            next_offset += 1 
            # Handle escaping - currently only bypasses special handling of characters
            if escaped:
                escaped = False
                char_lists[-1].append(next_char)
                continue
            elif next_char == '\\':
                escaped = True
                continue

            # Handle quoting
            if quoted:
                if next_char == quote_char:
                    # Append final quote, start new char_list
                    char_lists[-1].append(quote_char)
                    char_lists.append([])
                    quoted = False
                    quote_char = None
                    continue
                else:
                    char_lists[-1].append(next_char)
                    continue
            elif next_char in self.quotes:
                # Start new char_list for new token
                char_lists.append([])
                quoted = True
                quote_char = next_char
                char_lists[-1].append(quote_char)
                continue

            # Handle comments
            continue_parsing = False
            for comm in self.comments:
                if next_char == comm[0][0]:
                    new_offset = self._handle_comment(i, comm[1])
                    # Function returns offset of end of comment, None if it's not a comment
                    # Allows flexible handling of line vs block comments
                    if new_offset is not None:
                        # Start new char_list, since comment separates tokens
                        char_list_deque.append([])
                        next_offset = new_offset
                        continue_parsing = True
                        break

            if continue_parsing:
                continue

            # Handle separators - tokens that count as separate, even without whitespace
            continue_parsing = False
            for sep in self.separators:
                new_offset = cur_offset + len(sep)
                next_sep = self.source[cur_offset:new_offset]
                if next_sep == sep:
                    # If we find the separator, append and make a new char_list
                    # Ordering of comments is important
                    # TODO: Can we fix this? Or sort so we control it?
                    char_lists.append(list(next_sep))
                    char_lists.append([])
                    next_offset = new_offset
                    continue_parsing = True
                    break

            if continue_parsing:
                continue

            # Handle whitespace
            is_whitespace = False
            for c in self.white_space:
                if ord(next_char) >= c[0] and ord(next_char) < c[1]:
                    is_whitespace = True
                    break
            print next_char, cur_offset, char_lists[-1]
            if is_whitespace:
                char_lists.append([])
                while len(char_lists) > 1:
                    token = ''.join(char_lists.popleft())
                    # For each complete token, yield if its not empty
                    if len(token) > 0:
                        yield token
            else:
                # If this isn't whitespace, add it to the last token
                char_lists[-1].append(next_char)
        for char_list in char_lists:
            token = ''.join(char_list)
            # For each complete token, yield if its not empty
            if len(token) > 0:
                yield token
        # We finish here ... nothing else to do

def tests():
    a = Lexer()
    a.white_space =  [(32, 33), (10, 12)]
    a.quotes = ['\'', '"']
    a.separators = [",", "::="]
    a.source = "',::=\\','"
    a.length = len(a.source)
    print [x for x in a.tokens()]
