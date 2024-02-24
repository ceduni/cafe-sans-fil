const categories = [
  "Cafés",
  "Thés",
  "Boissons",
  "Snack"
];

const items = [
  {
    name: "Café filtre",
    price: 1.00,
    description: "Un bon petit café filtre pour se réveiller :)",
    variants: ["Petit", "Moyen", "Grand"],
    photo: "https://media1.coffee-webstore.com/img/cms/Blog/v60.jpg",
    category: 0
  },
  {
    name: "Café mocha (filtre)",
    price: 1.00,
    description: "Un délicieux café mocha avec une touche de magie!",
    variants: ["Petit", "Moyen", "Grand"],
    photo: "https://www.thespruceeats.com/thmb/Hz677yfVdPECquUOekjv0b9yXTE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/SES-mocha-4797918-step-04-599987714aec41aba02f1f870e900dd8.jpg",
    category: 0
  },
  {
    name: "Café mocha (expresso)",
    price: 2.00,
    description: "Un café monstrueusement délicieux 😋",
    variants: ["Petit", "Moyen", "Grand"],
    photo: "https://www.spoonfulofflavor.com/wp-content/uploads/2021/11/mocha-latte-recipe.jpg",
    category: 0
  },
  {
    name: "Nespresso",
    price: 2.00,
    description: "Un espresso magiquement intense, servi avec une cuillerée de crème fouettée",
    variants: ["Petit", "Moyen", "Grand"],
    photo: "https://www.nespresso.com/shared_res/agility/n-components/pdp/sku-main-info/coffee-sleeves/vl/orafio_L.png",
    category: 0
  },
  {
    name: "Espresso",
    price: 2.00,
    variants: ["Petit", "Moyen", "Grand"],
    description: "Un espresso audacieux et éclatant. Parfait pour démarrer votre journée avec énergie!",
    photo: "https://www.thespruceeats.com/thmb/HJrjMfXdLGHbgMhnM0fMkDx9XPQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/what-is-espresso-765702-hero-03_cropped-ffbc0c7cf45a46ff846843040c8f370c.jpg",
    category: 0
  },
  {
    name: "Café latte",
    price: 2.50,
    category: 0,
    variants: [],
    description: "Un latte légendaire avec un tourbillon de caramel, pour vous donner la motivation nécessaire pour conquérir vos cours!",
    photo: "https://www.allrecipes.com/thmb/Wh0Qnynwdxok4oN0NZ1Lz-wl0A8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/9428203-9d140a4ed1424824a7ddd358e6161473.jpg"
  },
  {
    name: "Americano glacé",
    price: 2.00,
    category: 0,
    variants: [],
    description: "Un americano glacé inspiré par les mystères de l'univers pour vous inspirer à poursuivre vos rêves les plus audacieux.",
    photo: "https://images.ctfassets.net/v601h1fyjgba/1vlXSpBbgUo9yLzh71tnOT/a1afdbe54a383d064576b5e628035f04/Iced_Americano.jpg"
  },
  {
    name: "Latte glacé",
    price: 2.50,
    category: 0,
    variants: [],
    description: "Un café latte glacé rafraîchissant avec une touche de sirop de menthe",
    photo: "https://images.ctfassets.net/v601h1fyjgba/4GLzOncHIe8rq3xY099cZ/dd17ce72ebb6fb01659c763fe64953db/Iced_Latte.jpg"
  },
  {
    name: "Chocolat chaud",
    price: 1.00,
    category: 0,
    variants: [],
    description: "Un chocolat chaud réconfortant, avec une touche de cannelle et de lait mousseux",
    photo: "https://belly-media.com/wp-content/uploads/2022/12/hot-chco.webp"
  },
  {
    name: "Menthe bio",
    price: 1.00,
    category: 1,
    variants: [],
  },
  {
    name: "Perles au jasmin",
    price: 1.00,
    category: 1,
    variants: [],
  },
  {
    name: "Chai Camellia",
    price: 1.00,
    category: 1,
    variants: [],
  },
  {
    name: "Nagashima bio",
    price: 1.00,
    category: 1,
    variants: [],
  },
  {
    name: "Matcha latte",
    price: 3.00,
    category: 1,
    variants: [],
  },
  {
    name: "Liqueur/Jus",
    price: 1.50,
    category: 2,
    variants: [],
  },
  {
    name: "Gatorade/Pure Leaf",
    price: 1.75,
    category: 2,
    variants: [],
  },
  {
    name: "Gatorade/Pure Leaf",
    price: 1.75,
    category: 2,
    variants: [],
  },
  {
    name: "Guru",
    price: 2.00,
    category: 2,
    variants: [],
  },
  {
    name: "Starbucks",
    price: 2.25,
    category: 2,
    variants: [],
  },
  {
    name: "Chocolat",
    price: 1.00,
    category: 3,
    variants: [],
  },
  {
    name: "Friandises",
    price: 1.50,
    category: 3,
    variants: [],
  },
  {
    name: "Noix",
    price: 2.00,
    category: 3,
    variants: [],
  },
  {
    name: "Ramen",
    price: 3.00,
    category: 3,
    variants: [],
  },
  {
    name: "Samosas",
    price: 3.25,
    category: 3,
    variants: [],
  },
  {
    name: "Pizza",
    price: 4.00,
    category: 3,
    variants: [],
  },
  {
    name: "Salade",
    price: 6.25,
    category: 3,
    variants: [],
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
      <img class="group-item-image" src="${item.photo}">
      <div class="group-item-info">
        <div class="group-item-info-main">
          <span class="group-item-name">${item.name}</span>
          <span class="group-item-price">${item.price.toFixed(2)}</span>
        </div>
        <div class="group-item-info-details">
          <span class="group-item-desc">${item.description}</span>
          <ul class="bare-list group-item-variants">
            ${item.variants.map(variant=> `<li class="group-item-variant">${variant}</li>`).join("")}
          </ul>
        </div>
      </div>
    </div>
    `).join("")
}


function createGroupBox(category, onclick) {
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
