#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import random
import time
import os

def emptyNet():
#s2.cmd("ovs-ofctl add-flow s2 priority=1,ip,nw_dst=10.0.0.2/24,actions=output:1")
   net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)
   c1 = net.addController('c1', controller=RemoteController, ip="127.0.0.1")
   c2 = net.addController('c2', controller=RemoteController, ip="127.0.0.2")
   host= [0]*80 
   for i in range(1,81):
      if i < 10 :
           mac = '00:00:00:00:00:0%s'%str(i)
           ip = '10.0.0.%s'%str(i)
           host[i-1]= net.addHost('h%s'%str(i), ip=ip, mac=mac)
      else:      
           mac = '00:00:00:00:00:%s'%str(i)
           ip = '10.0.0.%s'%str(i)
           host[i-1]= net.addHost('h%s'%str(i), ip=ip, mac=mac)
     
   
   server = net.addHost('server',  ip='10.0.0.99', mac='00:00:00:00:00:99')

   switch = [0]*21 
   for i in range(1,22):
      # x = i + 1
      if i < 10 :
          dpid='000000000000010%s'%str(i)
      else:      
          dpid='00000000000001%s'%str(i)     
      switch[i-1]= net.addSwitch('s%s'%str(i), dpid= dpid)
      


   print 'bulding links for Core switches from S1 to S4.'
   switch[0].linkTo( switch[4] )
   switch[0].linkTo( switch[6] )
   switch[0].linkTo( switch[8] )
   switch[0].linkTo( switch[10] )
   switch[1].linkTo( switch[4] )
   switch[1].linkTo( switch[6] )
   switch[1].linkTo(switch[8] )
   switch[1].linkTo( switch[10] )

   switch[2].linkTo(switch[5])
   switch[2].linkTo(switch[7])
   switch[2].linkTo(switch[9])
   switch[2].linkTo(switch[11])
   switch[3].linkTo(switch[5])
   switch[3].linkTo(switch[7])
   switch[3].linkTo(switch[9])
   switch[3].linkTo(switch[11])
   print 'bulding links for aggregation switches from S5 to S12.'
   switch[4].linkTo(switch[12])
   switch[4].linkTo(switch[13])
   switch[5].linkTo(switch[12])
   switch[5].linkTo(switch[13])
   switch[6].linkTo( switch[14] )
   switch[6].linkTo( switch[15] )
   switch[7].linkTo( switch[14] )
   switch[7].linkTo( switch[15] )

   switch[8].linkTo(switch[16])
   switch[8].linkTo(switch[17])
   switch[9].linkTo(switch[16])
   switch[9].linkTo(switch[17])
   switch[10].linkTo(switch[18])
   switch[10].linkTo(switch[19])
   switch[11].linkTo(switch[18])
   switch[11].linkTo(switch[19])
   switch[19].linkTo(switch[20])

   
   print 'bulding links between hosts and edge switches.'
   for i in range(12,20):
      if i == 12:
         for x in range(0,10):
            switch[i].linkTo(host[x])
      elif i == 13:
         for x in range(10,20):
            switch[i].linkTo(host[x])
      elif i == 14:
         for x in range(20,30):
            switch[i].linkTo(host[x])
      elif i == 15:
         for x in range(30,40):
            switch[i].linkTo(host[x])          
      elif i == 16:
          for x in range(40,50):
            switch[i].linkTo(host[x])
      elif i == 17:
          for x in range(50,60):
            switch[i].linkTo(host[x])
      elif i == 18:
          for x in range(60,70):
            switch[i].linkTo(host[x])
      elif i == 19:
          for x in range(70,80):
            switch[i].linkTo(host[x])
      else:
          pass     
   switch[12].linkTo(server)
                         

   
   net.build()
   c1.start()
   c2.start()
   for i in range(0,20):
     switch[i].start([c1])
   switch[20].start([c2])
   #net.start()
   enableSTP()
   info( '\n*** Starting web server ***\n')
   server = net.get('server')
   server.cmd('iperf -s -p 80 &')
   server.cmd('tcpdump tcp port 80 -i server-eth0 -w server.pcap &')
   #print ('\n*** Starting the attack simulation ***\n')

   print ('\n*** Starting the collection of the host info ***\n')
   i = 1
   while i < 81:
      try:
         client=net.get('h%s'%str(i)) 
       #client.cmdPrint('nohup python client.py 2&> c%s &' %str(i))
         client.cmdPrint('ping 10.0.0.50 -c1')
         time.sleep(5)
         i = i + 1
      except KeyboardInterrupt:
                              i = 81
   info( '*** Starting the simulation ***\n')
   #time.sleep(30)
   variable = raw_input('The simulation is being started by Clicking any kayboard button \n ')
   os.system('sudo python measure.py')
   net.pingAll()
   attacker = 73
   finish_time = 0
   start_time = time.time()
   while finish_time <= 180:
      for i in range(1,81):
         client=net.get('h%s'%str(i))
         if finish_time >= 20 and i == attacker:
            s20.cmd("ovs-ofctl add-flow s20 priority=10, in_port = 6, nw_src= 192.168.67.200/24,actions=controller")
            client.cmdPrint('sudo hping3 -c 10 --flood -p 80 10.0.0.99 -S --spoof 192.168.67.200')
         else: 
            client.cmdPrint('sudo hping3 -c 1 --flood 10.0.0.99 &')

         finish_time = time.time() - start_time
      
   print 'finish_time = ',finish_time
   
   net.staticArp()
   CLI( net )
   net.stop()

def enableSTP():
    """
    //HATE: Dirty Code
    """
    for x in range(1,22):
        cmd = "ovs-vsctl set Bridge s%s stp_enable=true" %x
        os.system(cmd)
        print cmd    

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
