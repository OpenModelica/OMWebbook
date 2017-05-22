# OMWebbook
An OpenModelica interactive notebook online

Requirements 

1) docker, To install docker see https://docs.docker.com/engine/installation/

To build OMWebbook

 1) clone the project
 2) cd OMWebbook
 3) docker build -t omwebbook .
After building the image omwebbook, we are now ready to run the OMWeb

To use it, run: 

>> docker run -d -p 80:80 omwebbook
