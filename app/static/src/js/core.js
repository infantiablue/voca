$(document).ready(function () {
	//Javascript to toggle the menu
	document.getElementById("nav-toggle").onclick = function () {
		document.getElementById("nav-content").classList.toggle("hidden");
	};

	$(".modal-overlay").click(toggleModal);
});

let toggleModal = () => {
	const modal = document.querySelector(".modal");
	modal.classList.toggle("opacity-0");
	modal.classList.toggle("pointer-events-none");
};

let preview = (word) => {
	$("#modal-content").empty();
	$("#modal-header").hide();
	$("#loading").show();
	toggleModal();
	$.get(`/api/lookup/${word}`)
		.done((data) => {
			$("#loading").hide();
			if (data.length > 0) {
				$("#modal-header").show();
				let r_count = 1;
				$("#modal-content").append(`<h1 class="text-yellow-600 text-3xl font-semibold uppercase">${word}</h1>`);
				for (let r of data) {
					$("#modal-content").append(`<h2 class="text-lg mt-2 font-semibold text-yellow-800">${r_count}.</h2>`);
					for (let e of r.sense) {
						$("#modal-content").append(`<h3 class="text-base text-gray-400 italic font-mono">(${e.lexical})</h3>`);
						for (let d of e.entry) {
							$("#modal-content").append(`<p></p>`);
							if (d.definition) $("#modal-content").append(`<p class="font-semibold">${d.definition}</p>`);
							$("#prevmodal-contentiew").append(`<p></p>`);
							for (let x of d.examples) $("#modal-content").append(`<p class="italic">-&nbsp;${x.text} </p>`);
						}
						$("#modal-content").append(`<p class="my-2"></p>`);
					}
					r_count++;
				}
			} else {
				$("#modal-content").append(`<h2 class="text-lg mt-2 font-semibold text-red-900">No entry found matching supplied </h2>`);
				$("#modal-header").hide();
			}
		})
		.fail(() => {
			$("#loading").hide();
			$("#modal-content").append(`<h2 class="text-lg mt-2 font-semibold text-red-900">No entry found matching supplied </h2>`);
			$("#modal-header").hide();
		});
};
