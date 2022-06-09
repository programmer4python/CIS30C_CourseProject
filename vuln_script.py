import nmap
import os

os.system('nmap -sA 127.0.0.1')
os.system('nmap -sV --script=/home/hyperquantum/Desktop/nmap3/vulscan/vulscan.nse 127.0.0.1')

