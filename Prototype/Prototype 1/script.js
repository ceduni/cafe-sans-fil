const categories = [
  "Boissons froides",
  "Boissons chaudes",
  "Sandwich",
  "Snack"
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
        <h4>${category.name}</h4>
        <div class="group-box-items">
            ${items(5 + randint(10))}
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
app.innerHTML = `
  <div class=content-wrapper>
    <h3>Menu</h3>
    <div id="menu" class="menu"></div>
  </div>
`;

setupMenu(app, document.querySelector("#menu"));

// evenement et publications

$(document).ready(function () {
  //  showing the clicked tab
  $('.tabs-control a').click(function () {
    $('.tabs-control a').removeClass('active');
    $(this).addClass('active');

    let currentTab = $(this).attr('href');
    $('.box').hide();
    $(currentTab).fadeIn();

    // saving current tab to local storage
    let index = $(this).index();
    localStorage.setItem('currentTab', index);
  });

  //  getting last current tab from storage
  let getTab = localStorage.getItem('currentTab');
  $('.tabs-control a').eq(getTab).addClass('active');
  $('.box').eq(getTab).show();
});
