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
  aLink.classList.remove("hidden");

  if (entry.img == "") {
    birdPhoto.src = "./assets/resources/egg.svg";
    birdPhoto.alt = "Bird Name Index";
    photoCredit.classList.add("hidden");
  } else {
    birdPhoto.src = entry.img;
    birdPhoto.classList.add("loading");
    birdPhoto.onload = () => {
      birdPhoto.alt = entry.en;
      photoCredit.classList.remove("hidden");
      birdPhoto.classList.remove("loading");
    };
  }
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
const aLink = results.querySelector("a");
const birdPhoto = results.querySelector(".bird-photo img");
const photoCredit = results.querySelector(".bird-photo span");

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
    render(list);
  } else {
    dropdownMenu.classList.add("hidden");
  }
});

reset.addEventListener("click", () => {
  dropdownMenu.classList.add("hidden");
});

dropdownMenu.addEventListener("click", (e) => {
  if (e.target.tagName !== "SPAN") return;

  let id;
  if (main.dataset.searchlang === "zh") {
    id = data.zh_index[e.target.textContent]["id"];
  } else if (main.dataset.searchlang === "jp") {
    id = data.jp_index[e.target.textContent];
  }

  if (id != null) {
    const speciesInfo = data.species[id];

    dropdownMenu.classList.add("hidden");
    input.value = e.target.textContent;
    showResult(speciesInfo);
  }
});
