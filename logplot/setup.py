from distutils.core import setup
import py2exe
import os
import matplotlib
    
setup(
    console=['logPlotController.py'],
    data_files = matplotlib.get_py2exe_datafiles(),
    options={
        'py2exe': {
            'includes': ['matplotlib',
                         'matplotlib.pyplot',
                         'matplotlib.figure',
                         'mpl_toolkits',
                         'pylab',
                         'datetime',
                         'matplotlib.backends.backend_tkagg',
                         ],
            'excludes': ['_gtkagg',
                         '_tkagg',
                         '_agg2',
                         '_cairo',
                         '_cocoaagg',
                         '_fltkagg'
                         '_gtk',
                         '_gtkcairo',
                         'Tkconstants',
                         'Tkinter',
                         'tcl'
                         ],
            'dll_excludes': ['tcl86t.dll',
                             'tk86t.dll'
                            ],
            'compressed':1,
            'bundle_files':2,
            'dist_dir':'../dist'
            }
        },
    )
