const categories = [
  "Boissons froides",
  "Boissons chaudes",
  "Sandwich",
  "Snack"
];

const items = [
  {
    name: "Café filtre",
    category: 0
  },
  {
    name: "Café mocha (filtre)",
    category: 0
  },
  {
    name: "Café mocha (expresso)",
    category: 0
  },
  {
    name: "Nespresso",
    category: 0
  },
  {
    name: "Espresso",
    category: 0
  },
  {
    name: "Café latte",
    category: 0
  },
  {
    name: "Americano glacé",
    category: 0
  },
  {
    name: "Latte glacé",
    category: 0
  },
  {
    name: "Chocolat chaud",
    category: 0
  },
]

function randint(max) {
  return Math.floor(Math.random() * max);
}

function div(options) {
  element = document.createElement("div");
  if (options.class) {
    element.classList.add(...options.class);
  }
  if (options.dataset) {
    Object.assign(element.dataset, options.dataset);
  }
  return element;
}

function createItem(category){
  return items.filter(item=>item.category == category).map(item=>
    `
    <div class="group-item">
    </div>
    `).join("")
}

function createGroupBox(category, onclick) {
  const items = (nb) =>
    `
    <div class="group-item">
    </div>
    `.repeat(nb);

  const groupBox = div({
    class: ["group-box"],
    dataset: {
      index: category.index
    }
  });
  groupBox.innerHTML = `
        <h4 class="group-box-title">${category.name}</h4>
        <div class="group-box-items">
            ${createItem(category.index)}
        </div>
        `;
  groupBox.tabIndex = 0;

  groupBox.addEventListener("click", (event) => {
    onclick(groupBox);
    groupBox.scrollIntoView(true);
  });

  return groupBox;
}

/**
 *
 * @param {HTMLElement} menu
 */
function setupMenu(app, menu) {
  let active = null;
  categories.forEach((category, index) => {
    menu.append(
      createGroupBox({ name: category, index: index }, (box) => {
        if (active && active !== box) {
          active.classList.remove("active");
        }
        if (active === box) {
          return;
        }
        active = box;
        active.classList.add("active");
        menu.classList.add("active");
        menu.dataset.selected = active.dataset.index;
      })
    );
  });

  app.addEventListener("click", (event) => {
    const target = event.target;

    if (!menu.contains(target) || target === menu) {
      menu.classList.remove("active");
      menu.dataset.selected = "";
      if (active) {
        active.classList.remove("active");
        active = null;
      }
    }
  });
}

const app = document.querySelector("#app");
const menu = document.querySelector("#menu");

setupMenu(app, menu);

function openTab(tabName) {
  var i, tabContent, tabLinks;
  tabContent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabContent.length; i++) {
    tabContent[i].classList.remove("active");
  }
  tabLinks = document.getElementsByClassName("tab");
  for (i = 0; i < tabLinks.length; i++) {
    tabLinks[i].classList.remove("active");
  }
  document.getElementById(tabName).classList.add("active");
  event.currentTarget.classList.add("active");
}
