let data = null;
let zhNames = [];
let jpNames = [];

fetch("./data/birds-data.json")
  .then((res) => res.json())
  .then((json) => {
    data = json;
    zhNames = Object.keys(data.zh_index);
    jpNames = Object.keys(data.jp_index);
  });

function searchZhNames(input) {
  if (input === "") return [];

  const results = [];

  for (let i = 0; i < zhNames.length; i++) {
    if (
      zhNames[i].includes(input) ||
      data.zh_index[zhNames[i]]["pinyin_initials"].includes(input)
    ) {
      results.push(zhNames[i]);

      if (results.length >= 20) {
        break;
      }
    }
  }
  return results;
}

function searchJpNames(input) {
  if (input === "") return [];

  const results = [];

  for (let i = 0; i < jpNames.length; i++) {
    if (toKatakana(jpNames[i]).includes(toKatakana(input))) {
      results.push(jpNames[i]);

      if (results.length >= 20) {
        break;
      }
    }
  }
  return results;
}

function toKatakana(str) {
  return str.replace(/[\u3041-\u3096]/g, function (ch) {
    return String.fromCharCode(ch.charCodeAt(0) + 0x60);
  });
}

function renderMenu(list) {
  dropdownMenu.innerHTML = list
    .map(
      (item) => `
    <span>${item}</span>
  `,
    )
    .join("");
}

function renderResult(name) {
  let id;
  if (main.dataset.searchlang === "zh") {
    id = data.zh_index[name]["id"];
  } else if (main.dataset.searchlang === "jp") {
    id = data.jp_index[name];
  }

  if (id != null) {
    const speciesInfo = data.species[id];

    dropdownMenu.classList.add("hidden");
    input.value = name;
    updateDom(speciesInfo);
  }
}

function updateDom(entry) {
  spanZh.textContent = entry.zh;
  spanEn.textContent = entry.en;
  spanJp.textContent = entry.jp;
  if (entry.rarity == "") {
    spanRarity.textContent = "普通";
  } else {
    spanRarity.textContent = entry.rarity;
  }

  let imgSrc = "./assets/resources/egg.svg";
  let imgAlt = "Bird Name Index";
  
  if (entry.img != "") {
    imgSrc = entry.img;
    imgAlt = entry.en;
  } else if ("img2" in entry && entry.img2 != "") {
    imgSrc = entry.img2;
    imgAlt = entry.en;
  }

  birdPhoto.src = imgSrc;
  birdPhoto.classList.add("loading");
  birdPhoto.onload = () => {
    birdPhoto.alt = imgAlt;
    birdPhoto.classList.remove("loading");
  };
}

const main = document.querySelector("main");
const langSwitch = document.getElementById("lang-switch");
const input = document.getElementById("search");
const reset = document.getElementById("reset");
const dropdownMenu = document.getElementById("dropdown");
const results = document.getElementById("results");

const spanZh = results.querySelector(".zh");
const spanEn = results.querySelector(".en");
const spanJp = results.querySelector(".jp");
const spanRarity = results.querySelector(".rarity");
const birdPhoto = results.querySelector(".bird-photo img");

langSwitch.addEventListener("click", () => {
  if (main.dataset.searchlang === "zh") {
    main.dataset.searchlang = "jp";
    input.placeholder = "输入日文鸟名";
    langSwitch.value = "日";
  } else if (main.dataset.searchlang === "jp") {
    main.dataset.searchlang = "zh";
    input.placeholder = "输入中文鸟名";
    langSwitch.value = "中";
  }
});

input.addEventListener("input", (e) => {
  if (!data) return;

  const value = e.target.value.trim();
  if (!value) {
    dropdownMenu.classList.add("hidden");
    dropdownMenu.innerHTML = "";
    return;
  }

  let list = [];
  if (main.dataset.searchlang === "zh") {
    list = searchZhNames(value);
  } else if (main.dataset.searchlang === "jp") {
    list = searchJpNames(value);
  }
  if (list.length > 0) {
    dropdownMenu.classList.remove("hidden");
    renderMenu(list);
  } else {
    dropdownMenu.classList.add("hidden");
  }
});

input.addEventListener("keypress", (e) => {
  const searchQuery = dropdownMenu.querySelectorAll("span");
  if (e.key==="Enter" && searchQuery.length===1) {
    renderResult(searchQuery[0].textContent);
  }
})

reset.addEventListener("click", () => {
  dropdownMenu.classList.add("hidden");
  input.value = "";
});

dropdownMenu.addEventListener("click", (e) => {
  if (e.target.tagName !== "SPAN") return;

  renderResult(e.target.textContent);
});
