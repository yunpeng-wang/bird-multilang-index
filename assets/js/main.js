let data = null;
let zhNames = [];

fetch("./data/birds-data.json")
  .then((res) => res.json())
  .then((json) => {
    data = json;
    zhNames = Object.keys(data.zh_index);
  });

function searchZhNames(input) {
  if (input === "") return [];

  const results = [];

  for (let i = 0; i < zhNames.length; i++) {
    if (zhNames[i].includes(input)) {
      results.push(zhNames[i]);

      if (results.length >= 20) {
        break;
      }
    }
  }
  return results;
}

function render(list) {
  dropdownMenu.innerHTML = list
    .map(
      (item) => `
    <span>${item}</span>
  `,
    )
    .join("");
}

function showResult(entry) {
  spanZh.textContent = entry.zh;
  spanEn.textContent = entry.en;
  spanJp.textContent = entry.jp;
  if (entry.rarity == "") {
    spanRarity.textContent = "普通";
  } else {
    spanRarity.textContent = entry.rarity;
  }
  aLink.href = entry.link;
}

const input = document.getElementById("search");
const reset = document.getElementById("reset");
const dropdownMenu = document.getElementById("dropdown");
const results = document.getElementById("results");

const spanZh = results.querySelector(".zh");
const spanEn = results.querySelector(".en");
const spanJp = results.querySelector(".jp");
const spanRarity = results.querySelector(".rarity");
const aLink = results.querySelector("a");

input.addEventListener("input", (e) => {
  if (!data) return;

  const value = e.target.value.trim();
  if (!value) {
    dropdownMenu.classList.add("hidden");
    dropdownMenu.innerHTML = "";
    return;
  }
  const list = searchZhNames(value);
  if (list.length > 0) {
    dropdownMenu.classList.remove("hidden");
    render(list);
  }
});

reset.addEventListener("click", () => {
  dropdownMenu.classList.add("hidden");
});

dropdownMenu.addEventListener("click", (e) => {
  if (e.target.tagName !== "SPAN") return;

  const id = data.zh_index[e.target.textContent];
  const speciesInfo = data.species[id];

  dropdownMenu.classList.add("hidden");
  input.value = e.target.textContent;
  showResult(speciesInfo);
});
