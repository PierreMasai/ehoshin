"""Some auxiliary functions linked with excel used in the other hoshin modules."""
from xlsxwriter.utility import xl_range
from collections import OrderedDict

import xlsxwriter
import os
import io
from hoshins import models


def leader_to_excel(items):
    """Create an excel stream for a leader.

    This function create an abstract of the comments
    from the items leaded by the user and save it in an excel way.
    No files are created, everything is kept in memory.

    Args:
        items (list): the items leaded by the user

    Returns:
        BytesIO: A buffered streams holding an excel file
    """
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    title_format = workbook.add_format({
        'font_size': 20,
        'bold': 1,
        'underline': 1,
        'align': 'center',
        'valign': 'vcenter',
    })

    headers_formats = workbook.add_format({
        'valign': 'vcenter',
        'align': 'center',
        'bold': 1,
        'bg_color': '#D9D9D9',
        'border': 2,
        'text_wrap': 1
    })

    headers = ['Type', 'Author', 'Text']

    base_format = workbook.add_format({
        'valign': 'vcenter',
        'text_wrap': 1,
        'border': 2,
        'shrink': 1,
    })

    center_format = workbook.add_format({
        'valign': 'vcenter',
        'text_wrap': 1,
        'border': 2,
        'shrink': 1,
        'align': 'center'
    })

    items = sorted(items, key=lambda it: it.id)
    index_item = 0
    for item in items:
        line_height = 25
        index_item += 1
        worksheet = workbook.add_worksheet("%d. %s" % (index_item, item.get_trunc_name(20)))
        worksheet.set_row(0, 30)
        worksheet.set_row(1, 30)
        worksheet.set_column('A:A', 4)
        worksheet.set_column('B:B', 6)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 120)

        cell_range = xl_range(0, 0, 0, 4)
        worksheet.merge_range(cell_range, 'Theme : ' + item.name, title_format)

        col = 1
        for header in headers:
            worksheet.write(2, col, header, headers_formats)
            col += 1

        parent = item.object_ptr
        comments = models.Comment.objects.filter(parent=parent)
        comments = sorted(comments, key=lambda co: co.id)

        line = 3
        for comment in comments:
            obj_com = comment.object_ptr
            author = obj_com.owner_temp

            if obj_com.owner_temp == "" and obj_com.owner:
                author = obj_com.owner.full_name

            cell_type = workbook.add_format({'border': 2})

            if comment.type == 'MO':
                cell_type.set_bg_color('yellow')
            elif comment.type == 'AD':
                cell_type.set_bg_color('green')
            elif comment.type == 'RE':
                cell_type.set_bg_color('red')

            worksheet.write(line, 1, "", cell_type)
            worksheet.write(line, 2, author, center_format)
            worksheet.write(line, 3, comment.text, base_format)

            height = 1
            for text_line in str(comment.text).split('\n'):
                height += (len(text_line) / 140)

            worksheet.set_row(line, line_height * height)
            line += 1

    workbook.close()
    output.seek(0)
    return output


def hoshin_to_excel(hoshin_id, team_name):
    """Create an excel stream of a hoshin.

    This function create an abstract of the hoshin given to
    him. No files are created, everything is kept in memory.

    Args:
        hoshin_id (int): The id of the hoshin.
        team_name (str): The name of the team.

    Returns:
        BytesIO: A buffered streams holding an excel file
    """
    line_height = 25

    hoshin = models.Hoshin.objects.get(id=hoshin_id)
    hoshin_name = hoshin.name + '.xlsx'

    team = models.Team.objects.get(name=team_name)

    if hasattr(team, 'references'):
        references = [ref.name for ref in team.references.all()]
    else:
        references = []

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet(hoshin.name)

    worksheet.set_row(0, 30)
    worksheet.set_row(1, 40)
    worksheet.set_column('B:B', 4)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 90)

    title_format = workbook.add_format({
        'font_size': 20,
        'bold': 1,
        'underline': 1,
    })

    headers_formats = workbook.add_format({
        'valign': 'vcenter',
        'align': 'center',
        'bold': 1,
        'bg_color': '#D9D9D9',
        'border': 2,
        'text_wrap': 1
    })

    base_format = {
        'valign': 'vcenter',
        'text_wrap': 1,
        'border': 2,
        'shrink': 1,
    }

    center_format = base_format.copy()
    center_format['align'] = 'center'

    base_format = workbook.add_format(base_format)
    center_format = workbook.add_format(center_format)
    empty_format = workbook.add_format({})

    col_begin = 1
    row_begin = 3

    cell_range = xl_range(row_begin-1, 6, row_begin-1, 5+len(references))
    worksheet.merge_range(cell_range, 'Links', headers_formats)

    cell_range = xl_range(0, 0, 0, 5)
    worksheet.merge_range(cell_range, hoshin.name, title_format)

    # cell_range = xl_range(1, 0, 1, 5)
    # worksheet.merge_range(cell_range, 'Message from CIO', cio_format)

    stamp_path = '/'.join(['ressources', team_name, 'hoshins', 'security_stamp.png'])
    if os.path.isfile(stamp_path):
        worksheet.insert_image('G1', stamp_path)

    headers = [
        'Ref.',
        'Hoshin theme',
        'Leader',
        'Implementation Targets',
    ]

    def int_to_letters(i):
        i += 1
        result = ''

        while i:
            i -= 1
            result = chr(i % 26 + ord('A')) + result
            i //= 26

        return result

    col = col_begin
    worksheet.set_row(row_begin, line_height)
    for cell in headers:
        worksheet.write(row_begin, col, cell, headers_formats)
        col += 1

    col += 1
    max_height = 0
    for cell in references:
        worksheet.write(row_begin, col, cell, headers_formats)
        max_height = max(max_height, len(str(cell))/10)
        letter = int_to_letters(col)
        worksheet.set_column(letter+':'+letter, 10)
        col += 1

    worksheet.set_row(row_begin, line_height * (max_height+1))
    lines = []

    item_number = 1
    items = hoshin.children.all()
    items = sorted(items, key=lambda it: it.id)

    for child in items:
        line = [
            item_number,
            child.name,
            child.leader,
            child.target,
            None
        ]

        item_refs = [ref.name for ref in child.object_ptr.references.all()]

        for ref in references:
            if ref in item_refs:
                rs = models.Referenceship.objects.get(
                        reference__name=ref,
                        object=child.object_ptr)
                index = rs.index and rs.index or 'v'

                line.append(index)
            else:
                line.append('')

        lines.append(line)
        item_number += 1

    row = row_begin+1

    for line in lines:
        col = col_begin
        max_height = 0

        for cell in line:
            if cell is None:
                format_cel = empty_format
            elif col < col_begin + 4:
                format_cel = col % 2 and center_format or base_format
            else:
                format_cel = center_format

            max_height = max(max_height, str(cell).count('\n'))
            worksheet.write(row, col, cell, format_cel)
            col += 1

        worksheet.set_row(row, line_height * (max_height+1))
        row += 1

    workbook.close()

    output.seek(0)

    return output, hoshin_name


def statistics_to_excel(hoshin_id):
    """Create an excel stream of an hoshin statistics.

    This function create an excel with the statistics
    of the hoshin given to him. No files are created,
    everything is kept in memory.

    Args:
        hoshin_id (int): The id of the hoshin.

    Returns:
        BytesIO: A buffered streams holding an excel file
    """
    hoshin = models.Hoshin.objects.get(id=hoshin_id)
    hoshin_name = hoshin.name + '_statistics.xlsx'

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet(hoshin.name)
    worksheet.set_row(0, 30)
    worksheet.set_column('B:B', 40)

    title_format = workbook.add_format({
        'font_size': 20,
        'bold': 1,
        'underline': 1,
    })

    headers_formats = workbook.add_format({
        'valign': 'vcenter',
        'align': 'center',
        'bold': 1,
        'bg_color': '#D9D9D9',
        'border': 2,
        'text_wrap': 1
    })

    base_format = {
        'valign': 'vcenter',
        'text_wrap': 1,
        'border': 2,
        'shrink': 1,
    }

    center_format = base_format.copy()
    center_format['align'] = 'center'

    base_format = workbook.add_format(base_format)
    cell_range = xl_range(0, 1, 0, 10)
    worksheet.merge_range(cell_range, 'Statistics ' + hoshin.name, title_format)

    cell_range = xl_range(3, 1, 3, 2)
    worksheet.merge_range(cell_range, 'General', headers_formats)

    values = OrderedDict([
        ['Themes', hoshin.nb_items],
        ['Concrete actions', hoshin.nb_implementation_priorities],
        ['Comments', hoshin.nb_comments],
        ['Users', hoshin.nb_users],
        ['One comment', hoshin.nb_commentators],
        ['Many comments', hoshin.nb_chatty_commentators]
    ])

    i = 4
    for key, val in values.items():
        worksheet.write(i, 1, key, base_format)
        worksheet.write(i, 2, val, base_format)
        i += 1

    i += 1
    cell_range = xl_range(i, 1, i, 2)
    worksheet.merge_range(cell_range, 'Number of comments per themes', headers_formats)
    i += 1

    nb_comments = hoshin.object_ptr.comments.count()
    worksheet.write(i, 1, 'Hoshin overall', base_format)
    worksheet.write(i, 2, nb_comments, base_format)
    i += 1

    for item in hoshin.children.all():
        nb_comments = item.object_ptr.comments.count()
        worksheet.write(i, 1, item.name, base_format)
        worksheet.write(i, 2, nb_comments, base_format)
        i += 1

    workbook.close()
    output.seek(0)

    return output, hoshin_name
