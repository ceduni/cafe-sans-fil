const categories = [
  "Sandwich",
  "Boissons chaudes",
  "Snack",
  "Boissons froides"
];

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
            ${items(5 + randint(10))}
        </div>
        `;
  groupBox.tabIndex = 0;

  groupBox.addEventListener("click", (event) => {
    onclick(groupBox);
    groupBox.scrollIntoView(false);
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
