import ocl
import camvtk
import time
import vtk
import datetime
import math
import random
import gc

def drawVertex(myscreen, p, vertexColor, rad=1):
    myscreen.addActor( camvtk.Sphere( center=(p.x,p.y,p.z), radius=rad, color=vertexColor ) )

def drawEdge(myscreen, e, edgeColor=camvtk.yellow):
    p1 = e[0]
    p2 = e[1]
    myscreen.addActor( camvtk.Line( p1=( p1.x,p1.y,p1.z), p2=(p2.x,p2.y,p2.z), color=edgeColor ) )

def drawFarCircle(myscreen, r, circleColor):
    myscreen.addActor( camvtk.Circle( center=(0,0,0), radius=r, color=circleColor ) )

def drawDiagram( myscreen, vd ):
    drawFarCircle(myscreen, vd.getFarRadius(), camvtk.pink)
    
    for v in vd.getGenerators():
        drawVertex(myscreen, v, camvtk.green, 2)
    for v in vd.getVoronoiVertices():
        drawVertex(myscreen, v, camvtk.red, 1)
    for v in vd.getFarVoronoiVertices():
        drawVertex(myscreen, v, camvtk.pink, 10)
    vde = vd.getVoronoiEdges()
    
    print " got ",len(vde)," Voronoi edges"
    for e in vde:
        drawEdge(myscreen,e, camvtk.cyan)

class VD:
    def __init__(self, myscreen):
        self.myscreen = myscreen
        self.generators = []
        self.verts=[]
        self.far=[]
        self.edges =[]
        self.DTedges =[]
        self.generatorColor = camvtk.green
        self.vertexColor = camvtk.red
        self.edgeColor = camvtk.cyan
        self.vdtext  = camvtk.Text()
        self.vdtext.SetPos( (50, myscreen.height-50) )
        self.Ngen = 0
        self.vdtext_text = ""
        self.setVDText()
        
        myscreen.addActor(self.vdtext)
        
    def setVDText(self):
        if len(self.generators) > 3:
            self.Ngen = len( self.generators )-3
        else:
            self.Ngen = 0
        self.vdtext_text = "Delaunay Triangulation, " + str(self.Ngen) + " generators."
        self.vdtext.SetText( self.vdtext_text )
        self.vdtext.SetSize(32)
        
    def setGenerators(self, vd):
        for g in self.generators:
            myscreen.removeActor(g)

        self.generators = []
        #gc.collect()
        for p in vd.getGenerators():
            gactor = camvtk.Sphere( center=(p.x,p.y,p.z), radius=0.5, color=self.generatorColor )
            self.generators.append(gactor)
            myscreen.addActor( gactor )
        self.setVDText()
        myscreen.render() 
    
    def setFar(self, vd):
        for p in vd.getFarVoronoiVertices():
            myscreen.addActor( camvtk.Sphere( center=(p.x,p.y,p.z), radius=4, color=camvtk.pink ) )
        myscreen.render() 
            
            
    def setVertices(self, vd):
        for p in self.verts:
            myscreen.removeActor(p)
            #p.Delete()
        self.verts = []
        #gc.collect()
        for p in vd.getVoronoiVertices():
            actor = camvtk.Sphere( center=(p.x,p.y,p.z), radius=0.08, color=self.vertexColor )
            self.generators.append(actor)
            myscreen.addActor( actor )
        myscreen.render() 
        
    def setEdges(self, vd):
        for e in self.edges:
            myscreen.removeActor(e)
            #e.Delete()
        self.edges = []
        #gc.collect()
        for e in vd.getEdgesGenerators():
            ofset = 0
            p1 = e[0]  
            p2 = e[1] 
            actor = camvtk.Line( p1=( p1.x,p1.y,p1.z), p2=(p2.x,p2.y,p2.z), color=self.edgeColor )
            myscreen.addActor(actor)
            self.edges.append(actor)
        myscreen.render() 
        
    def setDT(self,vd):
        for e in self.DTedges:
            myscreen.removeActor(e)
        self.DTedges = []
        #gc.collect()
        #print "dt-edges: ",vd.getDelaunayEdges()
        for e in vd.getDelaunayEdges():
            p1 = e[0]  
            p2 = e[1] 
            actor = camvtk.Line( p1=( p1.x,p1.y,p1.z), p2=(p2.x,p2.y,p2.z), color=camvtk.red )
            myscreen.addActor(actor)
            self.DTedges.append(actor)
        myscreen.render()
        
    def setAll(self, vd):
        #self.setVertices(vd)
        self.setGenerators(vd)
        self.setEdges(vd)
        self.setDT(vd)

def addVertexSlow(myscreen, vd, vod, p):        
    pass
    
if __name__ == "__main__":  
    print ocl.revision()
    myscreen = camvtk.VTKScreen()
    myscreen.camera.SetPosition(0.01, 0,  3000 ) # 1200 for far view, 300 for circle view
    myscreen.camera.SetFocalPoint(0, 0, 0)
    myscreen.camera.SetClippingRange(-100,3000)
    camvtk.drawOCLtext(myscreen)
    
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(myscreen.renWin)
    lwr = vtk.vtkPNGWriter()
    lwr.SetInput( w2if.GetOutput() )
    #w2if.Modified()
    #lwr.SetFileName("tux1.png")
    
    
    myscreen.render()
    random.seed(42)
    
    vd = ocl.VoronoiDiagram(130,10)
    
    vod = VD(myscreen)
    #vod.setAll(vd)
    drawFarCircle(myscreen, vd.getFarRadius(), camvtk.orange)
    #plist=[ocl.Point(61,61)  ]
    #plist.append(ocl.Point(-20,-20))
    #plist.append(ocl.Point(0,0)) 
    
    plist=[]
    
    
    #RANDOM points
    
    Nmax = 30
    rpos=[-50,-50]
    for n in range(Nmax):
        x=rpos[0]+60*random.random()
        y=rpos[1]+60*random.random()
        plist.append( ocl.Point(x,y) )
    
    
    # SQUARE
    Nmax = 30
    rpos=[50,-50]
    side=30
    pts=[ ocl.Point(rpos[0]-side,rpos[1]-side) , 
          ocl.Point(rpos[0]-side,rpos[1]+side) ,
          ocl.Point(rpos[0]+side,rpos[1]+side) , 
          ocl.Point(rpos[0]+side,rpos[1]-side)]
    for n in range(Nmax):
        t=float(n)/float(Nmax)
        for m in [ [0,1], [1,2] , [2,3] , [3,0] ]:
            
            p = t*pts[ m[0] ] + (1-t)*pts[ m[1] ]
            print t," : ",n,"edge",m,"point= ",p
            plist.append( p )
        #x=rpos[0]-rpos[0]/2+40*random.random()
        #y=rpos[1]-rpos[1]/2+40*random.random()
        #
    #exit()
    
    
    # REGULAR GRID
    
    rows = 10
    gpos=[-50,50]
    for n in range(rows):
        for m in range(rows):
            x=gpos[0]-gpos[0]/2+(60/rows)*n
            y=gpos[1]-gpos[1]/2+(60/rows)*m
            
            # rotation
            alfa = 0
            xt=x
            yt=y
            x = xt*math.cos(alfa)-yt*math.sin(alfa)
            y = xt*math.sin(alfa)+yt*math.cos(alfa)
            
            plist.append( ocl.Point(x,y) )
        
    random.shuffle(plist)
        
    # POINTS ON A CIRCLE
    #"""
    cpos=[50,50]
    npts = 100
    dalfa= 2*math.pi/npts
    dgamma= 10*2*math.pi/npts
    alfa=0
    ofs=10
    for n in range(npts):
        
        x=cpos[0]+(20)*math.cos(alfa)
        y=cpos[1]+(40)*math.sin(alfa)
        alfa = alfa+dalfa
        # rotation
        beta = 0
        xt=x
        yt=y
        x = xt*math.cos(beta)-yt*math.sin(beta)
        y = xt*math.sin(beta)+yt*math.cos(beta)
            
        
        plist.append( ocl.Point(x,y) )
        
            
    random.shuffle(plist)
    #"""

    
    
    n=1
    t_before = time.time() 
    sleep_time = 0
    render_interval = 500
    #vd.addVertexSite( ocl.Point(0,0,0) )
    for p in plist:
        #vod.setAll(vd)
        #myscreen.render()
        #time.sleep(sleep_time)
        print "PYTHON: adding generator: ",n," at ",p
        vd.addVertexSite( p )
        #vd.addVertexSiteRB( p )
        if n%render_interval == 0:
            vd.setDelaunayTriangulation()
            vod.setAll(vd)
            time.sleep(sleep_time)
        #w2if.Modified() 
        #lwr.SetFileName("frames/vd_dt_20_"+ ('%05d' % n)+".png")
        #lwr.Write()
        n=n+1
    t_after = time.time()
    calctime = t_after-t_before
    #print " VD done in ", calctime," s, ", calctime/Nmax," s per generator"
    vd.setDelaunayTriangulation()
    vod.setAll(vd)
    print "PYTHON All DONE."
    
    myscreen.render()    
    myscreen.iren.Start()
