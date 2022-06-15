import Reel from "./Reel.js";
import Symbol from "./Symbol.js";


function getData() {
    let symbols = [], won, returnCoef;

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/getState",
        async: false,
        // data: { param: input },
        success: function(response) {
            let arr = response.split(',');
            returnCoef = parseFloat(arr.pop())
            won = arr.pop();
            symbols = [];

            for (let i = 0, k = -1; i < arr.length; i++) {
                if (i % 3 === 0) {
                    k++;
                    symbols[k] = [];
                }

                symbols[k].push(arr[i]);
            }
        }
    });

    return [symbols, won, returnCoef];
}


export default class Slot {

	constructor(domElement, config = {}) {
		Symbol.preload();

		this.won = 0;
		this.returnCoef = 0.0;

		this.currentSymbols = [
			["death_star", "death_star", "death_star"],
			["death_star", "death_star", "death_star"],
			["death_star", "death_star", "death_star"],
			["death_star", "death_star", "death_star"],
			// ["death_star", "death_star", "death_star"],
		];

		this.nextSymbols = [
			["death_star", "death_star", "death_star"],
			["death_star", "death_star", "death_star"],
			["death_star", "death_star", "death_star"],
			["death_star", "death_star", "death_star"],
			// ["death_star", "death_star", "death_star"],
		];

		this.container = domElement;

		this.reels = Array.from(this.container.getElementsByClassName("reel")).map(
			(reelContainer, idx) =>
				new Reel(reelContainer, idx, this.currentSymbols[idx])
		);

		this.spinButton = document.getElementById("spin");
		this.spinButton.addEventListener("click", () => this.spin());

		this.autoPlayCheckbox = document.getElementById("autoplay");

		if (config.inverted) {
			this.container.classList.add("inverted");
		}

		this.config = config;
	}


	spin() {		
		this.currentSymbols = this.nextSymbols;

		const resp = getData();

		this.nextSymbols = resp[0];
		this.won = resp[1];
		this.returnCoef = resp[2];

		this.onSpinStart(this.nextSymbols);



		return Promise.all(
			this.reels.map((reel) => {
				reel.renderSymbols(this.nextSymbols[reel.idx]);
				return reel.spin();
			})
		).then(() => this.onSpinEnd(this.nextSymbols));
	}


	onSpinStart(symbols) {
		this.spinButton.disabled = true;

		this.config.onSpinStart?.(symbols);
	}

	
	onSpinEnd(symbols) {
		this.spinButton.disabled = false;

		this.config.onSpinEnd?.(symbols);

		document.getElementById("win").innerText = "WIN: " + this.won;
		document.getElementById("returnCoef").innerText = "Return coefficient: " + this.returnCoef;

		if (this.autoPlayCheckbox.checked) {
			return window.setTimeout(() => this.spin(), 200);
		}
	}
}
