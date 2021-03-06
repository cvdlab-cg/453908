//FRANCESCO PARIS   matricola 453908

/*** function that normalizes between 0 and 1 rgb values ***/
var normalizzaColore = function(rgb){
    return [rgb[0]/255,rgb[1]/255,rgb[2]/255];
};



//per risolvere l'esercizio ho inserito i dati topologici in una matrice quadrata (10x10).
//L'elemento aij rappresenta l'altezza. L'indice j della colonna rappresenta la coordinata x.
//L'indicie di riga i rappresenta la coordinata y.
//Sfruttando tali informazioni ho creato delle terne [x,y,z] che rappresentano i punti di controllo di curve di Bezier.
//Tali curve rappresentano, lungo l'asse delle x il profilo altimetrico del terreno.


var domain = INTERVALS(1)(32);
var domain2D = PROD1x1([INTERVALS(1)(16),INTERVALS(1)(16)]);

//var matrix = [[0,0,0], [5,3,0], [1,4,0]];

var matrix =[
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,40,0,0,0],
	[0,0,0,0,-5,-10,-3,-3,-8,0],
	[0,0,-2,0,0,0,-13,0,0,1],
	[0,0,0,0,25,0,0,0,0,0],
	[0,0,0,0,0,0,-7,0,0,0],
	[0,0,0,0,-7,-7,0,0,0,0],
	[0,0,0,0,0,25,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0]
];

var curve = new Array();


var creaCurve = function(){
    
  for (i=0; i <= 9; i++ ) {
     var punto1 = new Array();
     var punto2 = new Array();
     var punto3 = new Array();
     var punto4 = new Array();
     var punto5 = new Array();
     var punto6 = new Array();
     var punto7 = new Array();
     var punto8 = new Array();
     var punto9 = new Array();
     var punto10 = new Array(); 
  	 
  	 
  	 for(j=0; j<=9; j++){  	 
  	 	if(j===0){   	 	 
  	 	 punto1.push(j);
  	 	 punto1.push(i);
  	 	 punto1.push(matrix[i][j]);  	 	
  	 	}
  	 	if(j===1){  	 	 
  	 	 punto2.push(j);
  	 	 punto2.push(i);
  	 	 punto2.push(matrix[i][j]);  	 	
  	 	}
  	 	if(j===2){  	 	 
  	 	 punto3.push(j);
  	 	 punto3.push(i);
  	 	 punto3.push(matrix[i][j]);  	 	   	 
  	    }
  	    if(j===3){  	 	 
  	 	 punto4.push(j);
  	 	 punto4.push(i);
  	 	 punto4.push(matrix[i][j]);  	 	   	 
  	    }
  	    if(j===4){  	 	 
  	 	 punto5.push(j);
  	 	 punto5.push(i);
  	 	 punto5.push(matrix[i][j]);  	 	   	 
  	    }
  	    if(j===5){  	 	 
  	 	 punto6.push(j);
  	 	 punto6.push(i);
  	 	 punto6.push(matrix[i][j]);  	 	   	 
  	    }
  	    if(j===6){  	 	 
  	 	 punto7.push(j);
  	 	 punto7.push(i);
  	 	 punto7.push(matrix[i][j]);  	 	   	 
  	    }
  	    if(j===7){  	 	 
  	 	 punto8.push(j);
  	 	 punto8.push(i);
  	 	 punto8.push(matrix[i][j]);  	 	   	 
  	    }
  	    if(j===8){  	 	 
  	 	 punto9.push(j);
  	 	 punto9.push(i);
  	 	 punto9.push(matrix[i][j]);  	 	   	 
  	    }
  	    if(j===9){  	 	 
  	 	 punto10.push(j);
  	 	 punto10.push(i);
  	 	 punto10.push(matrix[i][j]);  	 	   	 
  	    }
  	    
  	 }//fine for di j
  	 
  	 var puntiControllo = new Array();
  	 puntiControllo.push(punto1);
  	 puntiControllo.push(punto2);
  	 puntiControllo.push(punto3);
  	 puntiControllo.push(punto4);
  	 puntiControllo.push(punto5);
  	 puntiControllo.push(punto6);
  	 puntiControllo.push(punto7);
  	 puntiControllo.push(punto8);
  	 puntiControllo.push(punto9);
  	 puntiControllo.push(punto10);
  	
  	 var c = BEZIER(S0)(puntiControllo);
  	 curve.push(c); 		 
  
  }//fine for i

}//Fine funzione Crea Curve; 






var disegnaCurve = function(){
	for(i=0;i<=9;i++){
		var curva = MAP(curve[i])(domain);
		//DRAW(curva)
	}
}









//lancio CreaCurve che inizializza l'array che contiene le varie curve di profilo
creaCurve();
//disegno le curve di livello
disegnaCurve();








//poi disegnare la superficie totale
var superficieTerreno = BEZIER(S1)([curve[0],curve[1],curve[2],curve[3],curve[4],curve[5],curve[6],curve[7],curve[8],curve[9]]);
var outSuperficieTerreno = MAP(superficieTerreno)(domain2D);
var outSuperficieTerrenoColor = COLOR(normalizzaColore([122,84,59]))(outSuperficieTerreno);
DRAW(outSuperficieTerrenoColor);









