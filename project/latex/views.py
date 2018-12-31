#################
#### imports ####
#################

from flask import flash, redirect, render_template, request, \
    session, url_for, Blueprint
from functools import wraps
from secrets import token_hex
import os
from subprocess import call


################
#### config ####
################

latex_blueprint = Blueprint(
    'latex', __name__,
    template_folder='templates'
)

################
#### routes ####
################

# route for handling the login page logic
@latex_blueprint.route('/latex', methods=['GET', 'POST'])
def latex():
    tmpfile = token_hex(16)
    tmpfile = 'tmp/' + tmpfile

    print(os.path.dirname(os.path.abspath(__file__)))
    imgUrl = 'test.png'

    if not os.path.exists(tmpfile):
        os.makedirs(tmpfile)

    latexPreambleString = \
    r'\\documentclass[preview,border={0pt 5pt 0pt 0pt}]{standalone}\n\
\usepackage[usenames,dvipsnames,svgnames,table]{xcolor} % use color\n\
\\usepackage{algpseudocode}\n\
\\usepackage{mathtools}\n\
\\usepackage{graphicx}\n\
\\usepackage{amssymb}\n\
\\usepackage{epstopdf}\n\
\\usepackage{amsmath}\n\
\\usepackage{amssymb}\n\
\\usepackage{float}\n\
\\usepackage[normalem]{ulem}\n\
\\usepackage{multirow}\n\
\\usepackage{booktabs}\n\
\\usepackage{wrapfig}\n\
\\usepackage{caption}\n\
\\usepackage{tikz}\n\
\\begin{document}'
    
    SVGText = ''
    latexEquation = ''
    textSize = '500'
    texColor=''
    error = None

    if request.method == 'POST':

        submittedPreamble = "%r"%request.form['latexPreamble']
        submittedPreamble = submittedPreamble.replace("'\\","").replace("'","")
        submittedEquation = "%r"%request.form['latexEquation']
        latexEquation = request.form['latexEquation']
        submittedEquation = submittedEquation.replace("\\\\","\\").replace("'","")
        texColor = request.form['texColor']
        textSize = request.form['latexSize']

        print(submittedEquation)

        file = open('{}/test.tex'.format(tmpfile),'w')
        for i in range(len(submittedPreamble.split('\\r\\n\\'))):
            file.write(submittedPreamble.split('\\r\\n\\')[i])
            file.write('\n')
        for j in range(len(submittedEquation.split('\\r\\n'))):
            file.write(submittedEquation.split('\\r\\n')[j])
            file.write('\n')
        file.write(r'\end{document}')
        file.close()

        call(['pdflatex', '-halt-on-error', '-output-directory', tmpfile, '{}/test.tex'.format(tmpfile)])

        if os.path.isfile('{}/test.pdf'.format(tmpfile)):

            call(['pdfcrop','{}/test.pdf'.format(tmpfile),'{}/test.pdf'.format(tmpfile)])
            call(['pdf2svg','{}/test.pdf'.format(tmpfile),'{}/test.svg'.format(tmpfile)])
            # cairosvg.svg2png(url='{}/test.svg'.format(tmpfile), write_to='{}/test.png'.format(tmpfile),dpi=int(300))

            with open('{}/test.svg'.format(tmpfile), 'r') as myfile:
                SVGText = myfile.read().replace('\n', '')
                SVGText = SVGText.split('viewBox')[1]
                SVGText = SVGText.replace('rgb(0%,0%,0%)',texColor)

        else: 

            error = 'Invalid LaTeX code. Check your syntax and try again.'

    
    return render_template('latex.html', latexSize=textSize, 
                                         error=error,
                                         texColor=texColor,
                                         latexEquation=latexEquation,
                                         SVGText=SVGText, 
                                         latexPreamble=latexPreambleString.replace('\\\\',"\\").replace('\\n\\',''))
