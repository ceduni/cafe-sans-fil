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

function generateFakeName(category) {
  const adjectives = {
    "Sandwich": ["Delicious", "Hearty", "Grilled", "Gourmet", "Spicy"],
    "Boissons chaudes": ["Warm", "Spiced", "Aromatic", "Creamy", "Rich"],
    "Snack": ["Crunchy", "Sweet", "Savory", "Tangy", "Nutty"],
    "Boissons froides": ["Iced", "Fruity", "Refreshing", "Chilled", "Sweet"]
  };
  const nouns = {
    "Sandwich": ["Sandwich", "Sub", "Wrap", "Panini", "Baguette"],
    "Boissons chaudes": ["Coffee", "Tea", "Latte", "Espresso", "Cappuccino"],
    "Snack": ["Chips", "Cookies", "Bars", "Nuts", "Fruits"],
    "Boissons froides": ["Smoothie", "Lemonade", "Iced Tea", "Soda", "Milkshake"]
  };

  const categoryAdjectives = adjectives[category] || ["Delicious"];
  const categoryNouns = nouns[category] || ["Item"];
  const adjective = categoryAdjectives[Math.floor(Math.random() * categoryAdjectives.length)];
  const noun = categoryNouns[Math.floor(Math.random() * categoryNouns.length)];
  return `${adjective} ${noun}`;
}

function generateFakePrice(category) {
  const priceRange = {
    "Sandwich": [5, 10],
    "Boissons chaudes": [2, 5],
    "Snack": [1, 4],
    "Boissons froides": [3, 7]
  };

  const range = priceRange[category] || [1, 15];
  let price = Math.random() * (range[1] - range[0]) + range[0];

  const endingType = Math.random();
  if (endingType < 0.9) {
    price = Math.floor(price) + (Math.random() < 0.5 ? 0.99 : 0.00);
    price = price.toFixed(2);
  } else {
    price = price.toFixed(2);
  }

  return `$${price}`;
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

  const items = (urls, count, category) => {
    return urls.slice(0, count).map(url => {
      const fakeName = generateFakeName(category);
      const fakePrice = generateFakePrice(category);
      return `
        <div>
          <img src="${url}" class="item-img" alt="item">
          <div class="item-name">${fakeName}</div>
          <div class="item-price">${fakePrice}</div>
        </div>
      `;
    }).join('');
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
        ${items(urlsToUse, itemCount, category.name)}
    </div>
    `;

  groupBox.tabIndex = 0;

  groupBox.addEventListener("click", (event) => {
    onclick(groupBox);
    setTimeout(() => {
      const groupBoxRect = groupBox.getBoundingClientRect();
      const distanceFromTop = 180;
      const topPositionToScroll = window.pageYOffset + groupBoxRect.top - distanceFromTop;
    
      window.scrollTo({
        top: topPositionToScroll,
        behavior: 'smooth'
      });
    }, 150);
    
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
