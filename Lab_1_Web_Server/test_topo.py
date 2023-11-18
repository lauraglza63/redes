from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build (self):
        "Create a custom topo."

        #Add host and switches
        leftHost = self.addHost( 'h1')
        rightHost = self.addHost( 'h2')
        centerSwitch = self.addSwitch('s1')

        #Add links
        self.addLink(leftHost, centerSwitch)
        self.addLink(centerSwitch, rightHost)

topos = {'my_topo': ( lambda: MyTopo() )}