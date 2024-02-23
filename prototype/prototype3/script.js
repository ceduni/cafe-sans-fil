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

function fetchImageUrls(category) {
  const filename = category.toLowerCase().replace(/\s+/g, '') + '.json';
  const filepath = `./assets/${filename}`;
  return fetch(filepath)
    .then(response => response.json())
    .then(data => data)
    .catch(error => console.error('Error fetching image URLs:', error));
}

async function createGroupBox(category, onclick) {
  const imageUrls = await fetchImageUrls(category.name).catch(error => {
    console.error('Error fetching image URLs:', error);
    return [];
  });

  const itemCount = 5 + randint(10);

  const items = (urls, count) => {
    return urls.slice(0, count).map(url =>
      `<img src="${url}" class="group-item" alt="Item Image">`
    ).join('');
  };

  const groupBox = div({
    class: ["group-box"],
    dataset: {
      index: category.index
    }
  });

  let urlsToUse = imageUrls;
  while (urlsToUse.length < itemCount) {
    urlsToUse = urlsToUse.concat(imageUrls);
  }

  groupBox.innerHTML = `
        <h4 class="group-box-title">${category.name}</h4>
        <div class="group-box-items">
            ${items(urlsToUse, itemCount)}
        </div>
        `;
  groupBox.tabIndex = 0;

  groupBox.addEventListener("click", (event) => {
    onclick(groupBox);
    // groupBox.scrollIntoView(false);
  });

  return groupBox;
}

/**
 *
 * @param {HTMLElement} menu
 */
async function setupMenu(app, menu) {
  let active = null;
  for (const category of categories) {
    const groupBox = await createGroupBox({ name: category, index: categories.indexOf(category) }, (box) => {
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
    });
    menu.append(groupBox);
  }

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
