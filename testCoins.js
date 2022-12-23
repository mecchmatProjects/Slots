<!DOCTYPE html>
<html>
<body>
<h2>JavaScript Map Objects</h2>
<p>Using Map.entries():</p>

<p id="demo"></p>

<script>

// Create a Map
const COINS = new Map([
  ["Xrp",0.4],
  ["Ada",0.31],
  ["Shiba",0.00000914],
  ["Doge",0.087],
  ["Gala",0.025],
  ["Sand",0.55],
  ["Mana",0.39],
  ["FTM",0.18],
  ["Trx",0.05],
  ["Eos",0.92],
  ["Hbar",0.0492],
  ["Ftt",1.5],
  ["GoldenBox",0]
  
]);

let N = 5;
let GoldenBoxValue = 500;


const coinPie = function(x){
  return Math.pow(x, 5) * 100 * 5 + 
         5 * Math.pow(x, 4) * (1-x) * 20 * 4 +
         10 * Math.pow(x, 3) * Math.pow(1-x,2) * 10 * 3 +
         10 * Math.pow(x, 2) * Math.pow(1-x,3) * 4 * 2 +
         5 * x * Math.pow(1-x,4);
}

const findCoinPie = function(a,b,t,eps=0.000001){
    
    let c = (a + b)/2;
    
    if (b-a)<eps:
        return c;
    
    if coinPie(c)>t{
        return findCoinPie(a,c,t,eps);
        }
    return findCoinPie(c,b,t,eps);
    }

const generateProbs = function(values, q=0.4){
    
    n = values.length;
    var probs = Array.apply(0, Array(n));
    
    var sum_prob = 0;
    var sum_out = 0;
    
    const minValue = Math.min.apply(Math, values) + 0.000001;
    
    for (let i = 0; i < n-1; i++) {
    		    if (values[i]  > minValue){ 
              const v = findCoinPie(0,0.5,q/(4*n)/values[i]);
              probs[i] = v;
              sum_out += coinPie(v) * values[i];
              sum_prob += v;
            }
    
    }
    sum_out = q - sum_out;
    sum_prob = 1 - sum_prob;
    
    return {sum_out:sum_out, sum_prob:sum_prob, probs:probs};  

}   
     
const findFreeProb = function(a,b,value,sum_prob,min_price,gb_val,eps=0.000001){
    
    var c = (a + b)/2
    var p1 = c;
    var p2 = sum_prob-c;
    if ((b-a)<eps){
        
        return {p1:p1,p2:p2};
    }
    
    val = Math.pow(p1,5) * gb_val + coinPie(p2) * min_price;
    
    //#print("vc:",val,c,sum_prob-c)
    
    if (val>value){
        return findFreeProb(a,c,value,sum_prob,min_price,gb_val,eps);
    }
    return findFreeProb(c,b,value,sum_prob,min_price,gb_val,eps);
} 


const generateRealProbs(coin_values){

   let minPrice = 500;
   let it =-1;
   let i = 0;
   for (const x of coin_values.values()) {
        if(x>0 && x <minPrice){
           minPrice = x;
           it = i;
        }
        i++;
   }

   const {sums, sum_prob, probs } = generateProbs(coin_values.values());
   
   const {p,p1} = findFreeProb(0,sum_prob,sums, sum_prob, min_price, GoldenBoxValue,0.000001);
    
   probs[-1] = p;
   probs[it] = p1;
  
   return probs;
}

//https://stackoverflow.com/questions/41654006/numpy-random-choice-in-javascript
function randomChoice(p) {
    let rnd = p.reduce( (a, b) => a + b ) * Math.random();
    return p.findIndex( a => (rnd -= a) < 0 );
}

function randomChoices(p, count) {
    return Array.from(Array(count), randomChoice.bind(null, p));
}

function generateValues(coin_values,probs){

  let result = randomChoices(coin_values.keys(), N, probs);
  return result;
}


function calculateWin(coins, coins_values){
     
     var resCoins = new Map();
     
     for (const x of coins){
        if (resCoins.has(x)){
        	resCoins[x] += 1;
        }
        else{
        	resCoins.set(x,1);
        }
     }
     
		let sumWin =0;
		     
    for (const pair of fruits.entries()) {
        const name = pair[0];
        const val = pair[1];
  	    if (v==1){
            sumWin += coins_values[k];
        }
        else if(v==2){
            sumWin += 4 * coins_values[k] * 2;
        }
        else if(v==3){
            sumWin += 10 * coins_values[k] * 3;
        }
        else if(v==4){
            sumWin += 20 * coins_values[k] * 4;
        }
        else if(v==5){
            sumWin += 100 * coins_values[k] * 5;
            if (name=="GoldenBox"){
                sumWin += GoldenBoxValue;
            }
        }
		}
		
		return sumWin; 
}


function testMonteCarlo(coin_values, n){
	let winSum = 0;
	let probs = generateRealProbs(coin_values);

  for (let i = 0; i < n-1; i++) {
                state = generateValues(coin_values,probs);
                w = calculateWin(state, coin_values);
                winSum += w;
	} 
	
	return winSum;
}
                

let n = 5;      
let w = testMonteCarlo(COINS,n);
let ratio = w/n;
let text="" + ratio;
           
                
 document.getElementById("demo").innerHTML = text;
</script>

</body>
</html>      
