import cellprocessing as cp
import tkFileDialog
import os
from skimage.util import img_as_float, img_as_int
from skimage.io import imsave


class ReportsManager(object):

    def __init__(self, parameters):
        self.keys = cp.stats_format(parameters.cellprocessingparams)
        self.average_G = None
        self.average_cell_E = None
        self.average_septum_E = None

    def generate_report_control(self, image_manager, cells_manager, fret_manager, path):
        
        cells = cells_manager.cells
        g_value = fret_manager.fret_G
        e_value = fret_manager.fret_E

        HTML_HEADER = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
                        "http://www.w3.org/TR/html4/strict.dtd">
                    <html lang="en">
                      <head>
                        <meta http-equiv="content-type" content="text/html; charset=utf-8">
                        <title>title</title>
                        <link rel="stylesheet" type="text/css" href="style.css">
                        <script type="text/javascript" src="script.js"></script>
                      </head>
                      <body>\n"""

        report = [HTML_HEADER]

        e_report = "<h2>Used E value: " + str(e_value) + "</h2>"
        report.extend(e_report)
        g_report = "<h2>Average G value: " + str(g_value) + "</h2>"
        report.extend(g_report)

        if len(cells) > 0:
            header = '<table>\n<th>Cell ID</th><th>Images'
            for k in self.keys:
                label, digits = k
                header = header + '</th><th>' + label
            header += '</th>\n'
            fret = ['\n<h1>FRET cells:</h1>\n' + header + '\n']
            donor = ['\n<h1>Donor cells:</h1>\n' + header + '\n']
            acceptor = ['\n<h1>Acceptor Cells:</h1>\n' + header + '\n']
            wt = ['\n<h1>wt Cells:</h1>\n' + header + '\n']
            discarded = ['\n<h1>Discarded Cells:</h1>\n' + header + '\n']

            sorted_keys = []
            for k in sorted(cells.keys()):
                sorted_keys.append(int(k))

            sorted_keys = sorted(sorted_keys)

            for k in sorted_keys:
                cell = cells[str(k)]

                if cell.channel == "both":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_fret_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_fret_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    fret.append(lin)

                elif cell.channel == "donor":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_donor_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_donor_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    donor.append(lin)

                elif cell.channel == "acceptor":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_acceptor_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_acceptor_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    acceptor.append(lin)

                elif cell.channel == "wt":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_wt_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_wt_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    wt.append(lin)

                elif cell.channel == "discard":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_discarded_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_discarded_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    discarded.append(lin)

            if len(fret) > 1:
                report.extend(fret)
                report.append("</table>\n")
            if len(donor) > 1:
                report.extend(donor)
                report.append("</table>\n")
            if len(acceptor) > 1:
                report.extend(acceptor)
                report.append("</table>\n")
            if len(wt) > 1:
                report.extend(wt)
                report.append("</table\n")
            if len(discarded) > 1:
                report.extend(discarded)
                report.append("</table>\n")

            report.append('</body>\n</html>')
        
        open(path + os.sep + "html_report.html", "w").writelines(report)

    def generate_report_experiment(self, image_manager, cells_manager, fret_manager, path):
        cells = cells_manager.cells
        g_value = fret_manager.fret_G
        cell_e = fret_manager.cell_E
        septum_e = fret_manager.septum_E

        HTML_HEADER = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
                        "http://www.w3.org/TR/html4/strict.dtd">
                    <html lang="en">
                      <head>
                        <meta http-equiv="content-type" content="text/html; charset=utf-8">
                        <title>title</title>
                        <link rel="stylesheet" type="text/css" href="style.css">
                        <script type="text/javascript" src="script.js"></script>
                      </head>
                      <body>\n"""

        report = [HTML_HEADER]

        g_report = "<h2>used G value: " + str(g_value) + "</h2>"
        report.extend(g_report)

        cell_e_report = "<h2>Average cell E value: " + str(cell_e) + "</h2>"
        report.extend(cell_e_report)
        septum_e_report = "<h2>Average septum E value: " + str(septum_e) + "</h2>"
        report.extend(septum_e_report)

        if len(cells) > 0:
            header = '<table>\n<th>Cell ID</th><th>Images'
            for k in self.keys:
                label, digits = k
                header = header + '</th><th>' + label
            header += '</th>\n'
            fret = ['\n<h1>FRET cells:</h1>\n' + header + '\n']
            donor = ['\n<h1>Donor cells:</h1>\n' + header + '\n']
            acceptor = ['\n<h1>Acceptor Cells:</h1>\n' + header + '\n']
            wt = ['\n<h1>wt Cells:</h1>\n' + header + '\n']
            discarded = ['\n<h1>Discarded Cells:</h1>\n' + header + '\n']

            sorted_keys = []
            for k in sorted(cells.keys()):
                sorted_keys.append(int(k))

            sorted_keys = sorted(sorted_keys)

            for k in sorted_keys:
                cell = cells[str(k)]

                if cell.channel == "both":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_fret_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_fret_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    fret.append(lin)

                elif cell.channel == "donor":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_donor_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_donor_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    donor.append(lin)

                elif cell.channel == "acceptor":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_acceptor_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_acceptor_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    acceptor.append(lin)

                elif cell.channel == "wt":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_wt_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_wt_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    wt.append(lin)

                elif cell.channel == "discarded":
                    cellid = str(int(cell.label))
                    img = img_as_float(cell.image)
                    imsave(path + "/_discarded_images" +
                           os.sep + cellid + '.png', img)
                    lin = '<tr><td>' + cellid + '</td><td><img src="./' + '_discarded_images/' + \
                          cellid + '.png" alt="pic" width="200"/></td>'

                    for stat in self.keys:
                        lbl, digits = stat
                        lin = lin + '</td><td>' + \
                            ("{0:." + str(digits) +
                             "f}").format(cell.stats[lbl])

                    lin += '</td></tr>\n'
                    discarded.append(lin)

            if len(fret) > 1:
                report.extend(fret)
                report.append("</table>\n")
            if len(donor) > 1:
                report.extend(donor)
                report.append("</table>\n")
            if len(acceptor) > 1:
                report.extend(acceptor)
                report.append("</table>\n")
            if len(wt) > 1:
                report.extend(wt)
                report.append("</table\n")
            if len(discarded) > 1:
                report.extend(discarded)
                report.append("</table>\n")

            report.append('</body>\n</html>')
        
        open(path + os.sep + "html_report.html", "w").writelines(report)

    def generate_report(self, setname, image_manager, cells_manager, fret_manager, path=None):

        if path is None:
            path = tkFileDialog.askdirectory()

        if setname == "Control":
            path = path + os.sep + "Report Control"
            if not os.path.exists(path + os.sep + "_fret_images"):
                os.makedirs(path + os.sep + "_fret_images")
            if not os.path.exists(path + os.sep + "_donor_images"):
                os.makedirs(path + os.sep + "_donor_images")
            if not os.path.exists(path + os.sep + "_acceptor_images"):
                os.makedirs(path + os.sep + "_acceptor_images")
            if not os.path.exists(path + os.sep + "_wt_images"):
                os.makedirs(path + os.sep + "_wt_images")
            if not os.path.exists(path + os.sep + "_discarded_images"):
                os.makedirs(path + os.sep + "_discarded_images")
            self.generate_report_control(image_manager, cells_manager, fret_manager, path)

        elif setname == "Experiment":
            path = path + os.sep + "Report Experiment"
            if not os.path.exists(path + os.sep + "_fret_images"):
                os.makedirs(path + os.sep + "_fret_images")
            if not os.path.exists(path + os.sep + "_donor_images"):
                os.makedirs(path + os.sep + "_donor_images")
            if not os.path.exists(path + os.sep + "_acceptor_images"):
                os.makedirs(path + os.sep + "_acceptor_images")
            if not os.path.exists(path + os.sep + "_wt_images"):
                os.makedirs(path + os.sep + "_wt_images")
            if not os.path.exists(path + os.sep + "_discarded_images"):
                os.makedirs(path + os.sep + "_discarded_images")
            self.generate_report_experiment(image_manager, cells_manager, fret_manager, path)
            imsave(path + os.sep + "heatmap.tif", img_as_int(fret_manager.fret_heatmap))
