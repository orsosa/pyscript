#!/usr/bin/env python
from sys import argv
from subprocess import Popen,call,PIPE
import shlex,os,platform
fext = ["png","gif","pdf"]

if (len(argv) <> 3): exit(1)
pic_dir=fdir = argv[1]
fname=argv[2]
osname=platform.system()
outdir = "%sout"%fname.split(".")[0]
if ( not os.path.isdir("%s"%outdir)): 
  if osname=="Windows": cmd=shlex.split("mkdir %s"%outdir)
  else: cmd="mkdir %s"%outdir
  print(cmd)
  call(cmd,shell=True)

fout = open("%s/%s"%(outdir,fname),"w")

csignw=""
csignl=""
if osname=="Windows": csignl = "%%"
else:  csignw = "%%"
fout.write("""%%
\\documentclass{beamer}
%%\\setbeamertemplate{navigation symbols}{}
\\usepackage{tikz}
\\usetikzlibrary{matrix}
\\usetikzlibrary{positioning}
\\tikzset{>=stealth}
\\setbeamercovered{invisible}
\\uselanguage{spanish}
\\languagepath{spanish}
\\deftranslation[to=spanish]{Example}{Ejemplo}
\\usepackage[utf8]{inputenc}
\\usetheme[hideothersubsections]{PaloAlto}
\\usecolortheme{albatross}

\\usepackage{epstopdf}	%% Included EPS files automatically converted to PDF to include with pdflatex
%%\\epstopdfsetup{update}
\\epstopdfDeclareGraphicsRule
%s{.gif}{png}{.png}{convert #1 \\OutputFile}
%s{.gif}{png}{.png}{C:/"Program Files"/ImageMagick-6.8.0-Q16/convert.exe #1 \\OutputFile} %%windows
\\DeclareGraphicsExtensions{.pdf, .jpeg, .jpg, .gif, .png}
\\graphicspath{{%s/}}	%% Root directory of the pictures 
\\newcommand{\\dv}[3][]{\\ensuremath{\\frac{d^{#1}#2}{d #3^{#1}}}}
\\newcommand{\\pdv}[3][]{\\ensuremath{\\frac{\\partial^{#1}#2}{\\partial #3^{#1}}}}
\\newcommand{\\eval}[3]{\\ensuremath{\\left. {#1} \\right|^{#3}_{#2} }}
\\newcommand{\\tcg}[1]{\\textcolor{green}{#1}}
\\newcommand{\\lrp}[1]{\\ensuremath{\\left( #1 \\right)}}


\\usepackage[makeroom]{cancel}
\\usepackage{listings}
\\usepackage{animate}

\\usepackage{appendixnumberbeamer}
\\setbeamertemplate{footline}[frame number]
\\begin{document}
\\title{Presentation}  
\\author{Orlando Soto Sandoval}
%%\\logo{\\includegraphics[scale=0.1]{funy_qc.png}}
\\date{\\today} 

\\begin{frame}
\\titlepage
\\end{frame}

"""%(csignl,csignw,pic_dir))

cnt=1
flist=[]
if osname != "Windows":
  cmd="ln -s `readlink -f %s` %s"%(pic_dir,outdir)
  print cmd
  call(cmd,shell=True)


for ext in fext:
  if osname=="Windows": cmd=shlex.split("dir /b %s\\\*.%s"%(fdir,ext))
  else: 
    cmd="find %s/*.%s -type f -not -name '*-converted-to.png'"%(fdir,ext)
    print cmd
  flist = flist + Popen(cmd,shell=True,stdout=PIPE).communicate()[0].split()

for name in flist:
  cnt=cnt+1
  fout.write("""%% slide %d
\\begin{frame}{slide %d}
\\begin{center}
\\includegraphics[width=\\linewidth,height=0.8\\textheight,keepaspectratio]{%s}
\\end{center}
\\end{frame}
 %%
 """%(cnt,cnt,name))


fout.write("\\end{document}")
fout.close()
 
if osname=="Windows": cmd=shlex.split("pdflatex -synctex=1 -interaction=nonstopmode --shell-escape --output-directory=%s %s/%s"%(outdir,output,fname))
else : cmd="pdflatex -synctex=1 -interaction=nonstopmode --shell-escape --output-directory=%s %s/%s"%(outdir,outdir,fname)
print(cmd)
call(cmd,shell=True)
call(cmd,shell=True)

print """
#################################################################################################
## Presentation '%s/%s.pdf' created, using pictures found inside folder '%s'  !!!#####
#################################################################################################
"""%(outdir,fname.split(".")[0],argv[1]) 

exit(0)
