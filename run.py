import os
import sys
from PySide2.QtCore import Qt, QCoreApplication
from settings import Settings
QCoreApplication.setOrganizationName("UFAL")
QCoreApplication.setOrganizationDomain("ufal.ms.mff.cuni.cz")
QCoreApplication.setApplicationName("Annotations")
if os.name == 'nt':
    sys.path.append(Settings.get_value('sox_path', r'C:\Program Files (x86)\sox-14-4-2'))
    os.environ["PATH"] += os.pathsep + r'C:\Program Files (x86)\sox-14-4-2'

from PySide2.QtGui import QPalette, QColor, QFont
from PySide2.QtWidgets import QApplication
from annotations import Annotations

def main():

    app = QApplication(sys.argv)
    app.setStyle("Fusion")    


    Settings.apply_settings()
    a = Annotations()
    a.show()

    exit(app.exec_())

if __name__ == '__main__':
    main()