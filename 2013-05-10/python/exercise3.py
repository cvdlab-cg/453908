#RUOTA
#la ruota è composta da spessore della gomma, spessore cerchio, raggi, piccola borchia lato raggi
# cilindro che regge la ruota e dietro disco dei freni


import sys
# racing car wheel

sys.path.append("/Users/francescoparis/Documents/larpy")

from pyplasm import *
import scipy
from scipy import *

#---------------------------------------------------------
def VERTEXTRUDE((V,coords)):
    """
        Utility function to generate the output model vertices in a 
        multiple extrusion of a LAR model.
        V is a list of d-vertices (each given as a list of d coordinates).
        coords is a list of absolute translation parameters to be applied to 
        V in order to generate the output vertices.
        
        Return a new list of (d+1)-vertices.
    """
    return CAT(AA(COMP([AA(AR),DISTR]))(DISTL([V,coords])))

def cumsum(iterable):
    # cumulative addition: list(cumsum(range(4))) => [0, 1, 3, 6]
    iterable = iter(iterable)
    s = iterable.next()
    yield s
    for c in iterable:
        s = s + c
        yield s

def larExtrude(model,pattern):
    V,FV = model
    d = len(FV[0])
    offset = len(V)
    m = len(pattern)
    outcells = []
    for cell in FV:
        # create the indices of vertices in the cell "tube"
        tube = [v + k*offset for k in range(m+1) for v in cell]
        # take groups of d+1 elements, via shifting by one
        rangelimit = len(tube)-d
        cellTube = [tube[k:k+d+1] for k in range(rangelimit)]
        outcells += [scipy.reshape(cellTube,newshape=(m,d,d+1)).tolist()]
    outcells = AA(CAT)(TRANS(outcells))
    outcells = [group for k,group in enumerate(outcells) if pattern[k]>0 ]
    coords = list(cumsum([0]+(AA(ABS)(pattern))))
    outVerts = VERTEXTRUDE((V,coords))
    newModel = outVerts, CAT(outcells)
    return newModel

def GRID(args):
    model = ([[]],[[0]])
    for k,steps in enumerate(args):
        model = larExtrude(model,steps*[1])
    V,cells = model
    verts = AA(list)(scipy.array(V) / AA(float)(args))
    return MKPOL([verts, AA(AA(lambda h:h+1))(cells), None])
#---------------------------------------------------------











#questa funzione disegna un cerchio di raggio r, sul piano z = h che può essere spostato
#delle quantita' dx e dy
def cerchio(r,h,dx,dy):
	def cerchio0(p):
		alfa = p[0]
		return [dx + r*COS(alfa), dy + r*SIN(alfa),h]
	return cerchio0



domain = INTERVALS(2*PI)(40);
dom1d = INTERVALS(1)(32);
dom2d = PROD([domain,dom1d]);

dom2db = PROD([domain,domain]);
c1 = cerchio(3.25,0,0,0);
cir1 = MAP(c1)(domain);

c2 = cerchio(3.25,3.6,0,0);
cir2 = MAP(c2)(domain);

c1c2 = CUBICHERMITE(S2)([c1,c2,[0,0,0],[0,0,0]]);
outc1c2 = MAP(c1c2)(dom2d);
outc1c2Color = COLOR(BLACK)(outc1c2);


c3 = cerchio(2.2,0,0,0);
cir3 = MAP(c3)(domain);

c4 = cerchio(2.2,3.6,0,0);
cir4 = MAP(c4)(domain);

#stondatura della ruota
c1c3 = CUBICHERMITE(S2)([c1,c3,[0,0,-1],[0,0,1]]);
outc1c3 = MAP(c1c3)(dom2d);
outc1c3Color = COLOR(BLACK)(outc1c3);

#stondatura della ruota
c2c4 = CUBICHERMITE(S2)([c2,c4,[0,0,-1],[0,0,1]]);
outc2c4 = MAP(c2c4)(dom2d);
outc2c4Color = COLOR(BLACK)(outc2c4);

#bordo cerchione
bordoCerchione1 = cerchio(2,0,0,0);
outbordoCerchione1 = MAP(bordoCerchione1)(domain);

bordoCerchione2 = cerchio(2,3.6,0,0);
outbordoCerchione2 = MAP(bordoCerchione2)(domain);

bordoCerchione1bordoCerchione2 = CUBICHERMITE(S2)([bordoCerchione1,bordoCerchione2,[0,0,0],[0,0,0]]);
outbordoCerchione1bordoCerchione2 = MAP(bordoCerchione1bordoCerchione2)(dom2d);

spessoreCerchione = CUBICHERMITE(S2)([c3,bordoCerchione1,[0,0,0],[0,0,0]]);
outspessoreCerchione = MAP(spessoreCerchione)(dom2d);

spessoreCerchione2 = CUBICHERMITE(S2)([c4,bordoCerchione2,[0,0,0],[0,0,0]]);
outspessoreCerchione2 = MAP(spessoreCerchione2)(dom2d);



#turbina di un areo (tappo del motore) o cerchio di una bicicletta
def cerchio2 (p):
    u,v = p
    return v*COS(u), v*SIN(u)


dom_u = INTERVALS(2*PI)(12)
dom_v = INTERVALS(2)(2)
dom = PROD([dom_u,dom_v])
cerchio2 = MAP(cerchio2)(dom)

#VIEW(cerchio)
r = SKELETON(1)(cerchio2)
rEstruso = PROD([r,Q(0.5)]);
rEstrusoColor = COLOR(WHITE)(rEstruso)
#VIEW(rEstruso)


cerchioBorchia = cerchio(1,0,0,0);
borchiaPiccolaCentroRuota = CUBICHERMITE(S2)([cerchioBorchia,[0,0,0],[0,0,0],[0,0,0]]);
outborchiaPiccolaCentroRuota = MAP(borchiaPiccolaCentroRuota)(dom2d);

cerchioBorchia2 = cerchio(1,3.6,0,0);
borchiaPiccolaCentroRuota2 = CUBICHERMITE(S2)([cerchioBorchia2,cerchioBorchia,[0,0,0],[0,0,0]]);
outborchiaPiccolaCentroRuota2 = MAP(borchiaPiccolaCentroRuota2)(dom2d);

cilindroRuota = CUBICHERMITE(S2)([cerchioBorchia2,[0,0,3.6],[0,0,0],[0,0,0]]);
outcilindroRuota = MAP(cilindroRuota)(dom2d); #tappo dietro

#disco del freno a disco
discoFreno = cerchio(1.5,3.6,0,0);
freniRuota = CUBICHERMITE(S2)([discoFreno,[0,0,3.6],[0,0,0],[0,0,0]]);
outFreniRuota = MAP(freniRuota)(dom2d); #tappo dietro


ruota = STRUCT([cir1,cir2,outc1c2Color,cir3, cir4, outc1c3Color,outc2c4Color,
outbordoCerchione1bordoCerchione2,outspessoreCerchione,outspessoreCerchione2,rEstrusoColor,
outborchiaPiccolaCentroRuota, outborchiaPiccolaCentroRuota2,outborchiaPiccolaCentroRuota2,outcilindroRuota,outFreniRuota
]);


#VIEW(ruota)



#----------------sotto codice macchina




#profilo laterale 
dom1d = INTERVALS(1)(32);
dom2d = PROD([dom1d, dom1d]);

lc1Sx = CUBICHERMITE(S1)([[0,-2.3,6.5],[12.3,-1.25,4.20],[1,0,0],[0,0,-0.3]]);
outlc1Sx = MAP(lc1Sx)(dom1d);

#tondo della punta
lc2Sx = CUBICHERMITE(S1)([[12.3,-1.25,4.20],[12.3,-1.25,2.5],[1,0,-0.5],[-1,0,-1]]);
outlc2Sx = MAP(lc2Sx)(dom1d);

lc3Sx = CUBICHERMITE(S1)([[12.3,-1.25,2.5],[0,-2.3,2],[-1,0,-0.5],[-1,0,-0.5]]);
outlc3Sx = MAP(lc3Sx)(dom1d);

lc1Dx = CUBICHERMITE(S1)([[0,2.3,6.5],[12.3,1.25,4.20],[1,0,0],[0,0,-0.3]]);
outlc1Dx = MAP(lc1Dx)(dom1d);

lc2Dx = CUBICHERMITE(S1)([[12.3,1.25,4.20],[12.3,1.25,2.5],[1,0,0],[-1,0,0]]);
outlc2Dx = MAP(lc2Dx)(dom1d);

lc3Dx = CUBICHERMITE(S1)([[12.3,1.25,2.5],[0,2.3,2],[-1,0,-0.5],[-1,0,-0.5]]);
outlc3Dx = MAP(lc3Dx)(dom1d);



lc4Sx = CUBICHERMITE(S1)([[0,-2.3,6.5],[-4.7,-2.5,6.5],[0,0,0],[0,0,0]]);
outlc4Sx = MAP(lc4Sx)(dom1d);

lc4Dx = CUBICHERMITE(S1)([[0,2.3,6.5],[-4.7,2.5,6.5],[0,0,0],[0,0,0]]);
outlc4Dx = MAP(lc4Dx)(dom1d);


lc5Sx = CUBICHERMITE(S1)([[-4.7,-2.5,6.5],[-7.7,-7,6.5],[1,0,0],[-1,0,0]]);
outlc5Sx = MAP(lc5Sx)(dom1d);

lc5Dx = CUBICHERMITE(S1)([[-4.7,2.5,6.5],[-7.7,7,6.5],[1,0,0],[-1,0,0]]);
outlc5Dx = MAP(lc5Dx)(dom1d);




#parte di sopra lc5Sx, lc6Sx (prese d'aria laterali)

lc6Sx = CUBICHERMITE(S1)([[-7.7,-7,6.5],[-13.4,-7,6.5],[1,0,0],[-1,0,0]]);
outlc6Sx = MAP(lc6Sx)(dom1d);

lc6Dx = CUBICHERMITE(S1)([[-7.7,7,6.5],[-13.4,7,6.5],[1,0,0],[-1,0,0]]);
outlc6Dx = MAP(lc6Dx)(dom1d);


#restringimento e abbassamento del bocchettone dell'aria parta alta
lc7Sx = CUBICHERMITE(S1)([[-13.4,-7,6.5],[-16.4,-5,5.5],[-1,0,0],[-1,0,1]]);
outlc7Sx = MAP(lc7Sx)(dom1d);
lc7Dx = CUBICHERMITE(S1)([[-13.4,7,6.5],[-16.4,5,5.5],[-1,0,0],[-1,0,1]]);
outlc7Dx = MAP(lc7Dx)(dom1d);

#bocchettone si richiude parta alta settore e1
lc8Sx = CUBICHERMITE(S1)([[-16.4,-5,5.5],[-20.4,-2.6,4],[-1,0,1],[-1,0,0]]);
outlc8Sx = MAP(lc8Sx)(dom1d);

lc8Dx = CUBICHERMITE(S1)([[-16.4,5,5.5],[-20.4,2.6,4],[-1,0,1],[-1,0,0]]);
outlc8Dx = MAP(lc8Dx)(dom1d);


#chiusura parte alta
lc9Sx = CUBICHERMITE(S1)([[-20.4,-2.6,4],[-24.4,-0.75,3.75],[-1,0,0],[-1,0,0]]);
outlc9Sx = MAP(lc9Sx)(dom1d);

lc9Dx = CUBICHERMITE(S1)([[-20.4,2.6,4],[-24.4,0.75,3.75],[-1,0,0],[-1,0,0]]);
outlc9Dx = MAP(lc9Dx)(dom1d);

#chiusura dietro parte alta
chiusuraDietroAlta = CUBICHERMITE(S1)([[-24.4,-0.75,3.75],[-24.4,0.75,3.75],[0,0,0],[0,0,0]]);
outChiusuraDietroAlta = MAP(chiusuraDietroAlta)(dom1d);


#buco pilota dall'alto (largo 400, lungo 700)

bucoPilotaAlto1 = CUBICHERMITE(S1)([[-4.7,-2,6.5],[-4.7,2,6.5],[0,0,0],[0,0,0]]);
outBucoPilotaAlto1 = MAP(bucoPilotaAlto1)(dom1d);

bucoPilotaAlto2 = CUBICHERMITE(S1)([[-11.7,-2,6.5],[-11.7,2,6.5],[0,0,0],[0,0,0]]);
outBucoPilotaAlto2 = MAP(bucoPilotaAlto2)(dom1d);

#raccordo del buco del pilota

raccordoBucoPilotaAlto1 = CUBICHERMITE(S1)([[-4.7,-2,6.5],[-11.7,-2,6.5],[0,0,0],[0,0,0]]);
outRaccordoBucoPilotaAlto1 = MAP(raccordoBucoPilotaAlto1)(dom1d);

raccordoBucoPilotaAlto2 = CUBICHERMITE(S1)([[-4.7,2,6.5],[-11.7,2,6.5],[0,0,0],[0,0,0]]);
outRaccordoBucoPilotaAlto2 = MAP(raccordoBucoPilotaAlto2)(dom1d);

#arco poggiatesta pilota (larga 300, alto 750)
basePoggiatestaPilota1 = CUBICHERMITE(S1)([[-11.7,-1.5,6.5],[-11.7,0,6.5],[0,0,0],[0,0,0]]);
outBasePoggiatestaPilota1 = MAP(basePoggiatestaPilota1)(dom1d);

basePoggiatestaPilota2 = CUBICHERMITE(S1)([[-11.7,0,6.5],[-11.7,1.5,6.5],[0,0,0],[0,0,0]]);
outBasePoggiatestaPilota2 = MAP(basePoggiatestaPilota2)(dom1d);

arcoPoggiatestaPilota1 = CUBICHERMITE(S1)([[-11.7,-1.5,6.5],[-11.7,0,7.5],[0,0,1],[0,1,0]]);
outArcoPoggiatestaPilota1 = MAP(arcoPoggiatestaPilota1)(dom1d);

arcoPoggiatestaPilota2 = CUBICHERMITE(S1)([[-11.7,0,7.5],[-11.7,1.5,6.5],[0,1,0],[0,0,-1]]);
outArcoPoggiatestaPilota2 = MAP(arcoPoggiatestaPilota2)(dom1d);

#spessore intorno al posto del pilota
#linea lunga verso il fondo della macchina
spessore1Sx = CUBICHERMITE(S1)([[-4.7,-2.5,6.5],[-8.2,-2.5,6.5],[0,0,0],[0,0,0]]);
outSpessore1Sx = MAP(spessore1Sx)(dom1d);

spessore1Dx = CUBICHERMITE(S1)([[-4.7,2.5,6.5],[-8.2,2.5,6.5],[0,0,0],[0,0,0]]);
outSpessore1Dx = MAP(spessore1Dx)(dom1d);


#linea che raccorda lo spessore con il buco del pilota
spessore2Sx = CUBICHERMITE(S1)([[-4.7,-2.5,6.5],[-4.7,-2,6.5],[0,0,0],[0,0,0]]);
outSpessore2Sx = MAP(spessore2Sx)(dom1d);

spessore2Dx = CUBICHERMITE(S1)([[-4.7,2.5,6.5],[-4.7,2,6.5],[0,0,0],[0,0,0]]);
outSpessore2Dx = MAP(spessore2Dx)(dom1d);

spessore3Sx = CUBICHERMITE(S1)([[-8.2,-2.5,6.5],[-8.2,-2,6.5],[0,0,0],[0,0,0]]);
outSpessore3Sx = MAP(spessore3Sx)(dom1d);

spessore3Dx = CUBICHERMITE(S1)([[-8.2,2.5,6.5],[-8.2,2,6.5],[0,0,0],[0,0,0]]);
outSpessore3Dx = MAP(spessore3Dx)(dom1d);

#parte alta  dello spessore intorno al pilota alta 700 (parte sopraelevata)
#parti del contorno esterno
spessore4Sx = CUBICHERMITE(S1)([[-8.2,-2.5,6.5],[-9.9,-2.5,7],[0,0,1],[-1,0,0]]);
outSpessore4Sx = MAP(spessore4Sx)(dom1d);

spessore4Dx = CUBICHERMITE(S1)([[-8.2,2.5,6.5],[-9.9,2.5,7],[0,0,1],[-1,0,0]]);
outSpessore4Dx = MAP(spessore4Dx)(dom1d);

#parti interne
spessore5Sx = CUBICHERMITE(S1)([[-8.2,-2,6.5],[-9.9,-2,7],[0,0,1],[-1,0,0]]);
outSpessore5Sx = MAP(spessore5Sx)(dom1d);

spessore5Dx = CUBICHERMITE(S1)([[-8.2,2,6.5],[-9.9,2,7],[0,0,1],[-1,0,0]]);
outSpessore5Dx = MAP(spessore5Dx)(dom1d);

#chiudo la fine del raccordo stondato
spessore6Sx = CUBICHERMITE(S1)([[-9.9,-2.5,7],[-9.9,-2,7],[0,0,0],[0,0,0]]);
outSpessore6Sx = MAP(spessore6Sx)(dom1d);

spessore6Dx = CUBICHERMITE(S1)([[-9.9,2.5,7],[-9.9,2,7],[0,0,0],[0,0,0]]);
outSpessore6Dx = MAP(spessore6Dx)(dom1d);


#porto la parte alta del contorno intorno al buco del pilota alla fine del buco del pilota
#parte esterna
spessore7Sx = CUBICHERMITE(S1)([[-9.9,-2.5,7],[-11.7,-2.5,7],[0,0,0],[0,0,0]]);
outSpessore7Sx = MAP(spessore7Sx)(dom1d);

spessore7Dx = CUBICHERMITE(S1)([[-9.9,2.5,7],[-11.7,2.5,7],[0,0,0],[0,0,0]]);
outSpessore7Dx = MAP(spessore7Dx)(dom1d);

#parte interna
spessore8Sx = CUBICHERMITE(S1)([[-9.9,-2,7],[-11.7,-2,7],[0,0,0],[0,0,0]]);
outSpessore8Sx = MAP(spessore8Sx)(dom1d);

spessore8Dx = CUBICHERMITE(S1)([[-9.9,2,7],[-11.7,2,7],[0,0,0],[0,0,0]]);
outSpessore8Dx = MAP(spessore8Dx)(dom1d);



totSpessoreIntornoPilota = STRUCT([outSpessore1Sx,outSpessore1Dx,outSpessore2Sx, outSpessore2Dx,
outSpessore3Sx,outSpessore3Dx,outSpessore4Sx, outSpessore4Dx,outSpessore5Sx,outSpessore5Dx,
outSpessore6Sx, outSpessore6Dx, outSpessore7Sx, outSpessore7Dx, outSpessore8Sx, outSpessore8Dx

]);



#cupola dietro pilota

arco2PoggiatestaPilota1 = CUBICHERMITE(S1)([[-13.4,-1.5,6],[-13.4,0,6],[0,0,0],[0,0,0]]);
outArco2PoggiatestaPilota1 = MAP(arco2PoggiatestaPilota1)(dom1d);

arco2PoggiatestaPilota2 = CUBICHERMITE(S1)([[-13.4,0,6],[-13.4,1.5,6],[0,0,0],[0,0,0]]);
outArco2PoggiatestaPilota2 = MAP(arco2PoggiatestaPilota2)(dom1d);


arco2PoggiatestaPilota3 = CUBICHERMITE(S1)([[-13.4,-1.5,6],[-13.4,0,7],[0,0,1],[0,1,0]]);
outArco2PoggiatestaPilota3 = MAP(arco2PoggiatestaPilota3)(dom1d);

arco2PoggiatestaPilota4 = CUBICHERMITE(S1)([[-13.4,0,7],[-13.4,1.5,6],[0,1,0],[0,0,-1]]);
outArco2PoggiatestaPilota4 = MAP(arco2PoggiatestaPilota4)(dom1d);

#linea che unisce i due archi
lineaUnioneDueArchi = CUBICHERMITE(S1)([[-13.4,0,7],[-11.7,0,7.5],[0,0,0],[0,0,0]]);
outlineaUnioneDueArchi = MAP(lineaUnioneDueArchi)(dom1d);


#ovale sopra la testa del pilota coordinata x = -12.55 ed altezza 10 (devo lasciare spazio per una sbombatura esterna)
#dimensioni largo 150, alto 200, spessore 0.2
#contorno interno
ovaleAlto1 = CUBICHERMITE(S1)([[-12.55,0,7.8],[-12.55,0, 9.8],[0,-1,0],[0,1,0]]);
outOvaleAlto1 = MAP(ovaleAlto1)(dom1d);

ovaleAlto2 = CUBICHERMITE(S1)([[-12.55,0,9.8],[-12.55,0,7.8],[0,1,0],[0,-1,0]]);
outOvaleAlto2 = MAP(ovaleAlto2)(dom1d);

#contorno esterno
ovaleAlto3 = CUBICHERMITE(S1)([[-12.55,0,7.6],[-12.55,0, 10],[0,-1,0],[0,1,0]]);
outOvaleAlto3 = MAP(ovaleAlto3)(dom1d);

ovaleAlto4 = CUBICHERMITE(S1)([[-12.55,0,7.6],[-12.55,0,10],[0,1,0],[0,-1,0]]);
outOvaleAlto4 = MAP(ovaleAlto4)(dom1d);

cupolaDietroPilota = STRUCT([outArco2PoggiatestaPilota1,outArco2PoggiatestaPilota2, outArco2PoggiatestaPilota3,outArco2PoggiatestaPilota4,
outOvaleAlto1, outOvaleAlto2,outOvaleAlto3,outOvaleAlto4
  ]);
  
  
#raccordo la parte alta della macchina

linea1raccordo =  CUBICHERMITE(S1)([[-12.55,0,10],[-15.55,0,10],[0,0,0],[0,0,0]]);
outlinea1raccordo = MAP(linea1raccordo)(dom1d);

linea2raccordo = CUBICHERMITE(S1)([[-15.55,0,10],[-24.4,0,3.75],[0,0,0],[0,0,0]]);
outlinea2raccordo = MAP(linea2raccordo)(dom1d);

linea3raccordo = CUBICHERMITE(S1)([[-12.55,0,7.6],[-13.25,0,7.6],[0,0,0],[0,0,0]]);
outlinea3raccordo = MAP(linea3raccordo)(dom1d);

linea4raccordo = CUBICHERMITE(S1)([[-13.25,0,7.6],[-13.4,0,7],[-1,0,0],[0,0,-1]]);
outlinea4raccordo = MAP(linea4raccordo)(dom1d);



raccordoParteAlta = STRUCT([outlinea1raccordo,outlinea2raccordo,outlinea3raccordo,outlinea4raccordo]);  
  

#continuo bocchettoni verso parte bassa

bocchettoniLinea1 = CUBICHERMITE(S1)([[-7.7,-7,6.5],[-7.7,-7,0.5],[0,0,0],[0,0,0]]);
outbocchettoniLinea1 = MAP(bocchettoniLinea1)(dom1d);

bocchettoniLinea1Dx = CUBICHERMITE(S1)([[-7.7,7,6.5],[-7.7,7,0.5],[0,0,0],[0,0,0]]);
outbocchettoniLinea1Dx = MAP(bocchettoniLinea1Dx)(dom1d);

bocchettoniLinea2 = CUBICHERMITE(S1)([[-7.7,-7,0.5],[-20.7,-7,0.5],[0,0,0],[0,0,0]]);
outbocchettoniLinea2 = MAP(bocchettoniLinea2)(dom1d);

bocchettoniLinea2Dx = CUBICHERMITE(S1)([[-7.7,7,0.5],[-20.7,7,0.5],[0,0,0],[0,0,0]]);
outbocchettoniLinea2Dx = MAP(bocchettoniLinea2Dx)(dom1d);


#pezzo basso finale piattaforma nera

bocchettoniLinea3 = CUBICHERMITE(S1)([[-24.4,0,0.5],[-24.4,-5,0.5],[0,0,0],[0,0,0]]);
outbocchettoniLinea3 = MAP(bocchettoniLinea3)(dom1d);

bocchettoniLinea3Dx = CUBICHERMITE(S1)([[-24.4,0,0.5],[-24.4,5,0.5],[0,0,0],[0,0,0]]);
outbocchettoniLinea3Dx = MAP(bocchettoniLinea3Dx)(dom1d);


bocchettoniLinea4 = CUBICHERMITE(S1)([[-24.4,-5,0.5],[-22.4,-5,0.5],[0,0,0],[0,0,0]]);
outbocchettoniLinea4 = MAP(bocchettoniLinea4)(dom1d);

bocchettoniLinea4Dx = CUBICHERMITE(S1)([[-24.4,5,0.5],[-22.4,5,0.5],[0,0,0],[0,0,0]]);
outbocchettoniLinea4Dx = MAP(bocchettoniLinea4Dx)(dom1d);


bocchettoniLinea5 = CUBICHERMITE(S1)([[-22.4,-5,0.5],[-20.7,-7,0.5],[1,0,0],[0,-1,0]]);
outbocchettoniLinea5 = MAP(bocchettoniLinea5)(dom1d);

bocchettoniLinea5Dx = CUBICHERMITE(S1)([[-22.4,5,0.5],[-20.7,7,0.5],[1,0,0],[0,-1,0]]);
outbocchettoniLinea5Dx = MAP(bocchettoniLinea5Dx)(dom1d);


#collego le parti esterne del muso davanti con la parte bassa dei bocchettoni
#(provo con una curva di Hermite)

bocchettoniLinea6 = CUBICHERMITE(S1)([[-7.7,-7,0.5],[0,-2.3,2],[1,0,0],[1,0,0]]);
outbocchettoniLinea6 = MAP(bocchettoniLinea6)(dom1d);

bocchettoniLinea6Dx = CUBICHERMITE(S1)([[-7.7,7,0.5],[0,2.3,2],[1,0,0],[1,0,0]]);
outbocchettoniLinea6Dx = MAP(bocchettoniLinea6Dx)(dom1d);


#linea cambio di colore 
bocchettoniLinea7 = CUBICHERMITE(S1)([[-7.7,-7,2],[0,-2.3,2],[1,0,0],[1,0,0]]);
outbocchettoniLinea7 = MAP(bocchettoniLinea7)(dom1d);

bocchettoniLinea7Dx = CUBICHERMITE(S1)([[-7.7,7,2],[0,2.3,2],[1,0,0],[1,0,0]]);
outbocchettoniLinea7Dx = MAP(bocchettoniLinea7Dx)(dom1d);



bocchettoniBassi = STRUCT([outbocchettoniLinea1,outbocchettoniLinea2,outbocchettoniLinea1Dx,
outbocchettoniLinea2Dx,outbocchettoniLinea3, outbocchettoniLinea3Dx,outbocchettoniLinea4, outbocchettoniLinea4Dx,
outbocchettoniLinea5, outbocchettoniLinea5Dx,outbocchettoniLinea6,outbocchettoniLinea6Dx,
outbocchettoniLinea7,outbocchettoniLinea7Dx

]);



#alettone dietro altezza da terra 950
#linea alta dietro (linea d'inizio della stondatura)
alettoneDietro1 = CUBICHERMITE(S1)([[-26.4,5,9.5],[-26.4,-5,9.5],[0,0,0],[0,0,0]]);
outalettoneDietro1 = MAP(alettoneDietro1)(dom1d);

#linea Bassa Avanti (linea finale della stondatura)
alettoneDietro2 = CUBICHERMITE(S1)([[-22.4,5,7.5],[-22.4,-5,7.5],[0,0,0],[0,0,0]]);
outalettoneDietro2 = MAP(alettoneDietro2)(dom1d);

#unisco con stondatura linea di fine e di inizio
alettoneDietro3 = BEZIER(S1)([[-26.4,-5,9.5],[-26.4,-5,7.5],[-22.4,-5,7.5]]);
outalettoneDietro3 = MAP(alettoneDietro3)(dom1d);

alettoneDietro3Dx = BEZIER(S1)([[-26.4,5,9.5],[-26.4,5,7.5],[-22.4,5,7.5]]);
outalettoneDietro3Dx = MAP(alettoneDietro3Dx)(dom1d);

#completo rettangolo intorno alla stondatura
alettoneDietro4 = CUBICHERMITE(S1)([[-26.4,-5,9.5],[-22.4,-5,9.5],[0,0,0],[0,0,0]]);
outalettoneDietro4 = MAP(alettoneDietro4)(dom1d);

alettoneDietro4Dx = CUBICHERMITE(S1)([[-26.4,5,9.5],[-22.4,5,9.5],[0,0,0],[0,0,0]]);
outalettoneDietro4Dx = MAP(alettoneDietro4Dx)(dom1d);

alettoneDietro5 = CUBICHERMITE(S1)([[-26.4,-5,7.5],[-22.4,-5,7.5],[0,0,0],[0,0,0]]);
outalettoneDietro5 = MAP(alettoneDietro5)(dom1d);

alettoneDietro5Dx = CUBICHERMITE(S1)([[-26.4,5,7.5],[-22.4,5,7.5],[0,0,0],[0,0,0]]);
outalettoneDietro5Dx = MAP(alettoneDietro5Dx)(dom1d);

alettoneDietro6 = CUBICHERMITE(S1)([[-26.4,-5,9.5],[-26.4,-5,7.5],[0,0,0],[0,0,0]]);
outalettoneDietro6 = MAP(alettoneDietro6)(dom1d);

alettoneDietro6Dx = CUBICHERMITE(S1)([[-26.4,5,9.5],[-26.4,5,7.5],[0,0,0],[0,0,0]]);
outalettoneDietro6Dx = MAP(alettoneDietro6Dx)(dom1d);

alettoneDietro7 = CUBICHERMITE(S1)([[-22.4,-5,9.5],[-22.4,-5,7.5],[0,0,0],[0,0,0]]);
outalettoneDietro7 = MAP(alettoneDietro7)(dom1d);

alettoneDietro7Dx = CUBICHERMITE(S1)([[-22.4,5,9.5],[-22.4,5,7.5],[0,0,0],[0,0,0]]);
outalettoneDietro7Dx = MAP(alettoneDietro7Dx)(dom1d);

alettoneDietro8 = CUBICHERMITE(S1)([[-26.4,5,7.5],[-26.4,-5,7.5],[0,0,0],[0,0,0]]);
outalettoneDietro8 = MAP(alettoneDietro8)(dom1d);


alettoneDietro9 = CUBICHERMITE(S1)([[-26.4,-5,7.5],[-26.4,-5,3.5],[0,0,0],[0,0,0]]);
outalettoneDietro9 = MAP(alettoneDietro9)(dom1d);

alettoneDietro9Dx = CUBICHERMITE(S1)([[-26.4,5,7.5],[-26.4,5,3.5],[0,0,0],[0,0,0]]);
outalettoneDietro9Dx = MAP(alettoneDietro9Dx)(dom1d);

#stondatura che collega la parte bassa dell'alettone alla parte bassa della macchina
alettoneDietro10 = BEZIER(S1)([[-26.4,-5,3.5],[-26.4,-5,0.5],[-24.4,-5,0.5]]);
outalettoneDietro10 = MAP(alettoneDietro10)(dom1d);

alettoneDietro10Dx = BEZIER(S1)([[-26.4,5,3.5],[-26.4,5,0.5],[-24.4,5,0.5]]);
outalettoneDietro10Dx = MAP(alettoneDietro10Dx)(dom1d);



alettoneDietro = STRUCT([outalettoneDietro1,outalettoneDietro2,outalettoneDietro3,outalettoneDietro3Dx,
outalettoneDietro4,outalettoneDietro4Dx,outalettoneDietro5,outalettoneDietro5Dx, outalettoneDietro6, outalettoneDietro6Dx,
outalettoneDietro7, outalettoneDietro7Dx,outalettoneDietro8,outalettoneDietro9, outalettoneDietro9Dx,outalettoneDietro10,
outalettoneDietro10Dx

]);






#alettone davanti
alettoneDavanti1 = BEZIER(S1)([[12.3,-7,2],[12.5,0,1.4],[12.3,7,2]]);
outalettoneDavanti1 = MAP(alettoneDavanti1)(dom1d);

#rettangoli ai lati dell'alettone
#lati bassi esterni
lato1AlettoneDavantiSx = CUBICHERMITE(S1)([[12.3,-7,2],[7.3,-7,2],[0,0,0],[0,0,0]]);
outlato1AlettoneDavantiSx = MAP(lato1AlettoneDavantiSx)(dom1d);

lato1AlettoneDavantiDx = CUBICHERMITE(S1)([[12.3,7,2],[7.3,7,2],[0,0,0],[0,0,0]]);
outlato1AlettoneDavantiDx = MAP(lato1AlettoneDavantiDx)(dom1d);

#lati alti Esterni
lato2AlettoneDavantiSx = CUBICHERMITE(S1)([[12.3,-7,2.5],[7.3,-7,2.5],[0,0,0],[0,0,0]]);
outlato2AlettoneDavantiSx = MAP(lato2AlettoneDavantiSx)(dom1d);

lato2AlettoneDavantiDx = CUBICHERMITE(S1)([[12.3,7,2.5],[7.3,7,2.5],[0,0,0],[0,0,0]]);
outlato2AlettoneDavantiDx = MAP(lato2AlettoneDavantiDx)(dom1d);


#qui inserire la ruota
rigaDiametroRuota = CUBICHERMITE(S1)([[12.3,7,2],[0.3,7,2],[0,0,0],[0,0,0]]);
outrigaDiametroRuota = MAP(rigaDiametroRuota)(dom1d);

#righe di chiusura verticali
lato3AlettoneDavantiSx = POLYLINE([[12.3,-7,2],[12.3,-7,2.5]]);
lato3AlettoneDavantiDx = POLYLINE([[12.3,7,2],[12.3,7,2.5]]);
lato4AlettoneDavantiSx = POLYLINE([[7.3,-7,2],[7.3,-7,2.5]]);
lato4AlettoneDavantiDx = POLYLINE([[7.3,7,2],[7.3,7,2.5]]);





congiunzioneLatoSxDxAlettone = CUBICHERMITE(S1)([[7.3,-7,2.5],[7.3,7,2.5],[0,0,0],[0,0,0]]);
outcongiunzioneLatoSxDxAlettone = MAP(congiunzioneLatoSxDxAlettone)(dom1d);

#raccordi laterale alettone davanti
raccordoLateraliAlettoneDavantiSx = CUBICHERMITE(S1)([[7.3,-7,2.5],[12.3,-7,2],[0,0,-1],[1,0,0]]);
outraccordoLateraliAlettoneDavantiSx = MAP(raccordoLateraliAlettoneDavantiSx)(dom1d);


raccordoLateraliAlettoneDavantiDx = CUBICHERMITE(S1)([[7.3,7,2.5],[12.3,7,2],[0,0,-1],[1,0,0]]);
outraccordoLateraliAlettoneDavantiDx = MAP(raccordoLateraliAlettoneDavantiDx)(dom1d);



alettoneDavanti = STRUCT([outalettoneDavanti1,outlato1AlettoneDavantiSx,outlato1AlettoneDavantiDx,
outlato2AlettoneDavantiSx, outlato2AlettoneDavantiDx,lato3AlettoneDavantiSx,
lato3AlettoneDavantiDx, lato4AlettoneDavantiSx, lato4AlettoneDavantiDx,outcongiunzioneLatoSxDxAlettone,
outraccordoLateraliAlettoneDavantiSx,outraccordoLateraliAlettoneDavantiDx  ]);




#


ruotaR = R([2,3])(PI/2)(ruota);

#ruoteDavanti
ruotaRT1 = T([1,2,3])([3.5,9,3])(ruotaR);
ruotaRT1S = S([2])([-1])(ruotaRT1)
#ruoteDietro
ruotaRT2 = T([1])([-28])(ruotaRT1);
ruotaRT2S = S([2])([-1])(ruotaRT2);


asse1 = CYLINDER([0.2,14])(8);
asse1R = R([2,3])(PI/2)(asse1)
asse1RT = T([1,2,3])([3.5,9,3])(asse1R);
asse2RT = T([1])([-28])(asse1RT);



#macchina totale
totlPezzo1 = STRUCT([outlc1Sx, outlc2Sx, outlc3Sx,outlc1Dx, outlc2Dx, outlc3Dx,outlc4Sx,outlc4Dx,outlc5Sx,outlc5Dx,outlc6Sx,
outlc6Dx, outlc7Sx, outlc7Dx, outlc8Sx,outlc8Dx,outlc9Sx,outlc9Dx,outChiusuraDietroAlta, 

outBucoPilotaAlto1,outBucoPilotaAlto2,outRaccordoBucoPilotaAlto1,outRaccordoBucoPilotaAlto2,

outBasePoggiatestaPilota1,outBasePoggiatestaPilota2, outArcoPoggiatestaPilota1,outArcoPoggiatestaPilota2,

totSpessoreIntornoPilota,

cupolaDietroPilota,
outlineaUnioneDueArchi,
raccordoParteAlta,
bocchettoniBassi,
alettoneDietro,
alettoneDavanti,


ruotaRT1,ruotaRT1S,ruotaRT2,ruotaRT2S,
asse1RT,asse2RT  


]);
VIEW(totlPezzo1);




















