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
    "Sandwich": [1, 5],
    "Boissons chaudes": [1, 3],
    "Snack": [1, 4],
    "Boissons froides": [1, 3]
  };

  const range = priceRange[category] || [1, 15];
  let price = Math.random() * (range[1] - range[0]) + range[0];

  const endingType = Math.random();
  if (endingType < 0.33) {
    price = Math.floor(price) + 0.99;
  } else if (endingType < 0.66) {
    price = Math.floor(price) + 0.50;
  } else {
    price = Math.floor(price);
  }
  price = price.toFixed(2);

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


document.querySelectorAll('.status').forEach(function(element) {
  element.addEventListener('click', function() {
    this.classList.toggle('active');
  });
});

document.addEventListener('click', function(e) {
  if (e.target.classList.contains('item-img') && e.target.closest('.group-box.active')) {
    const groupBox = e.target.closest('.group-box.active');
    showItemDetails(e.target, groupBox);
    e.stopPropagation();
  } else if (!e.target.closest('.item-details-view')) {
    resetGroupBoxPadding();
    closeDetailsView(e);
  }
});

function showItemDetails(image, groupBox) {
  closeAllDetailsViews();
  groupBox.classList.add('details-active');

  const detailsView = document.createElement('div');
  detailsView.innerHTML = `
    <img src="${image.src}" class="detailed-img">
    <div class="item-details">
      <div class="description">Item Description</div>
      <div class="size-options">Sizes: S, M, L</div>
      <button class="order-btn">Order</button>
      <button class="add-cart-btn">Add to Cart</button>
    </div>
  `;
  detailsView.classList.add('item-details-view');
  groupBox.appendChild(detailsView);
}

function closeAllDetailsViews() {
  const openDetailsViews = document.querySelectorAll('.item-details-view');
  openDetailsViews.forEach(view => {
    view.parentNode.classList.remove('details-active');
    view.remove();
  });
}

function resetGroupBoxPadding() {
  document.querySelectorAll('.group-box').forEach(groupBox => {
    groupBox.classList.remove('details-active');
  });
}
function closeDetailsView(event) {
  const detailsViews = document.querySelectorAll('.item-details-view');
  detailsViews.forEach(view => {
    if (!view.contains(event.target)) {
      view.remove();
    }
  });
}

document.addEventListener('DOMContentLoaded', function() {
  const cafeCommunication = document.querySelector('.cafe-communication');
  let originalTop = cafeCommunication.offsetTop;
  let isFixed = false;

  function applyFixedPosition() {
    cafeCommunication.classList.add('cafe-communication-fixed');
    isFixed = true;
  }

  function removeFixedPosition() {
    cafeCommunication.classList.remove('cafe-communication-fixed');
    isFixed = false;
  }

  document.addEventListener('scroll', function() {
    const scrollY = window.scrollY || window.pageYOffset;
    if (scrollY >= originalTop && !isFixed) {
      applyFixedPosition();
    } else if (scrollY < originalTop && isFixed) {
      removeFixedPosition();
    }
  });

  window.addEventListener('resize', function() {
    if (isFixed) {
      removeFixedPosition();
      applyFixedPosition();
    }
  });
});
