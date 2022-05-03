import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None



def markdown_to_html(content):
    parsed=content
    
    heading_list=re.finditer('#{1,6}(.*?)*\r', content)
    bold_list=re.finditer('\*{2}(.*?)\*{2}', content)
    emphasis_list=re.finditer('\*{1}(.*?)\*{1}', content)
    link_list=re.finditer('\[(.*?)\]\((.*?)\)', content)


    if heading_list is not None:
        ocurrences=[heading.group() for heading in heading_list]
        filter=re.compile('[\s#]') # remove markdown characters, clean text

        for heading in ocurrences:
            level=len(re.search('#{1,6}', heading).group())
            parsed=parsed.replace(heading, f"<h{level}>{filter.sub('',heading)}</h{level}>")

    if bold_list is not None:
        ocurrences=[bold.group() for bold in bold_list]
        filter=re.compile('[*]')

        for bold in ocurrences:
            parsed=parsed.replace(bold, f"<b>{filter.sub('',bold)}</b>")

    if emphasis_list is not None:
        ocurrences=[emphasis.group() for emphasis in emphasis_list]
        filter=re.compile('[*]')

        for emphasis in ocurrences:
            parsed=parsed.replace(emphasis, f"<em>{filter.sub('',emphasis)}</em>")
    if link_list is not None:
        ocurrences=[link.group() for link in link_list]
        filter=re.compile('[\[\)]')

        for link in ocurrences:
            name,href=[filter.sub("", link_piece) for link_piece in link.split("](")]
            parsed=parsed.replace(link, f"<a href='{href}'>{name}</a>")
            
    return parsed