find . -type f ! -regex ".*/\..*" ! -name ".*" ! -name "*~" ! -name 'src2pdf' ! -name '*pyc' ! -name '__init__.py' |
sed 's/^\..//' |                 ## Change ./foo/bar.src to foo/bar.src

while read  i; do                ## Loop through each file

   ## This command will include the file in the PDF
    echo "\subsubsection{../src/$i}"
    echo "\lstinputlisting{../src/$i}" 
done