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


//publication

var like = document.getElementById("fav");
var mrk = document.getElementById("bookmrk");
var cmt = document.getElementById("comment");
var modal = document.getElementById("cmtModal");

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));

function likePost() {
  if (like.style.color == "var(--red)") {
    like.style.color = "var(--darkone)";
    like.style.animation = "";
  } else {
    like.style.color = "var(--red)";
    like.style.animation = "pop .5s alternate 0s ease-in-out";
  }
}

function mrkPost() {
  if (mrk.style.color == "var(--blue)") {
    mrk.style.color = "var(--darkone)";
    mrk.style.animation = "";
  } else {
    mrk.style.color = "var(--blue)";
    mrk.style.animation = "pop .5s alternate 0s ease-in-out";
  }
}

var span = document.getElementsByClassName("close")[0];

function cmtPost() {
 cmt.style.animation = "pop .5s alternate 0s ease-in-out";
 modal.style.display = "block";
 modal.style.animation = "totop .5s alternate 0s ease-in-out"; 
}

async function openCmt() {
 modal.style.animation = "tobottom .5s alternate 0s ease-in-out";
 await sleep(500);
 modal.style.display = "none"
 cmt.style.animation = "";
}

window.onclick = function(event) {
 if (event.target == modal) {
   modal.style.display = "none";
   }
}

// document.addEventListener('DOMContentLoaded', (event) => {
//   let tabContent = document.getElementById('tab1'); // Conteneur de l'onglet
//   let userPost = document.querySelector('.pubcontainer'); // Élément à cloner

//   // Cloner userPost et ajouter au DOM trois fois
//   for (let i = 0; i < 3; i++) { // Changez le 0 à la quantité de clones que vous souhaitez créer
//     let clone = userPost.cloneNode(true); // Cloner l'élément
//     clone.id = 'userPostClone' + i; // Attribuer un nouvel ID au clone pour éviter le doublon d'ID
//     tabContent.appendChild(clone); // Ajouter le clone au conteneur
//   }
// });

document.addEventListener('DOMContentLoaded', (event) => {
  let tabContent = document.getElementById('tab1'); // Le conteneur parent de l'onglet
  let postContainer = document.querySelector('.pubcontainer'); // Le post original que vous voulez cloner

  // Informations pour les différents posts
  const postsData = [
    { userName: 'User1', postText: 'fkajbdbfk kjfa kkjfhkshk djkf' },
    { userName: 'User2', postText: 'Bla bla bla' },
    { userName: 'User3', postText: 'Bkjsdff fhdsjjfkd' }
  ];

  // Assurez-vous d'abord de vider le contenu de tab1, ou de supprimer le post original si nécessaire
  // tabContent.innerHTML = ''; // Décommentez cette ligne si vous voulez supprimer le contenu original

  // Cloner et modifier le contenu pour chaque post
  postsData.forEach((postData, index) => {
    // Cloner le conteneur de post original
    let clone = postContainer.cloneNode(true); 

    // Modifier le contenu du clone
    let userNameSpan = clone.querySelector('#user');
    let postTextSpan = clone.querySelector('#txt');

    userNameSpan.textContent = postData.userName; // Modifier le nom d'utilisateur
    postTextSpan.textContent = postData.postText; // Modifier le texte du post

    // Attribuer un nouvel ID au clone pour éviter des doublons (si nécessaire)
    clone.id = 'userPostClone' + index;

    // Ajouter le clone au conteneur de l'onglet
    tabContent.appendChild(clone);
  });
});


//evenements

// const randomDay = () => {
//   let random_day = Math.floor(Math.random() * 30);
//   console.log('your random day is: ' + random_day);
// }

// const randomMonth = () => {
//   let months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
//   let random_month = months[Math.floor(Math.random() * 12)];
//   console.log('your random month is: ' + random_month);
//   return random_month;
// }

// Chatbox

function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

//Sondage

$( document ).ready( function() {
  var button = $('.button');
  var slider = $('.slider');
  
  button.on('click', function(e) {
    
    if ( slider.hasClass('closed') ) {
      button.text('Hide Him!');
      slider.toggleClass('closed');
    } else {
      button.text('No, Bring Him Back!');
      slider.toggleClass('closed');
    }
    
  });
  
}); 

// poll

jQuery('.mm-prev-btn').hide();

	var x;
	var count;
	var current;
	var percent;
	var z = [];

	init();
	getCurrentSlide();
	goToNext();
	goToPrev();
	getCount();
	// checkStatus();
	// buttonConfig();
	buildStatus();
	deliverStatus();
	submitData();
	goBack();

	function init() {
		
		jQuery('.mm-survey-container .mm-survey-page').each(function() {

			var item;
			var page;

			item = jQuery(this);
			page = item.data('page');

			item.addClass('mm-page-'+page);
			//item.html(page);

		});

	}

	function getCount() {

		count = jQuery('.mm-survey-page').length;
		return count;

	}

	function goToNext() {

		jQuery('.mm-next-btn').on('click', function() {
			goToSlide(x);
			getCount();
			current = x + 1;
			var g = current/count;
			buildProgress(g);
			var y = (count + 1);
			getButtons();
			jQuery('.mm-survey-page').removeClass('active');
			jQuery('.mm-page-'+current).addClass('active');
			getCurrentSlide();
			checkStatus();
			if( jQuery('.mm-page-'+count).hasClass('active') ){
				if( jQuery('.mm-page-'+count).hasClass('pass') ) {
					jQuery('.mm-finish-btn').addClass('active');
				}
				else {
					jQuery('.mm-page-'+count+' .mm-survery-content .mm-survey-item').on('click', function() {
						jQuery('.mm-finish-btn').addClass('active');
					});
				}
			}
			else {
				jQuery('.mm-finish-btn').removeClass('active');
				if( jQuery('.mm-page-'+current).hasClass('pass') ) {
					jQuery('.mm-survey-container').addClass('good');
					jQuery('.mm-survey').addClass('okay');
				}
				else {
					jQuery('.mm-survey-container').removeClass('good');
					jQuery('.mm-survey').removeClass('okay');
				}
			}
			buttonConfig();
		});

	}

	function goToPrev() {

		jQuery('.mm-prev-btn').on('click', function() {
			goToSlide(x);
			getCount();			
			current = (x - 1);
			var g = current/count;
			buildProgress(g);
			var y = count;
			getButtons();
			jQuery('.mm-survey-page').removeClass('active');
			jQuery('.mm-page-'+current).addClass('active');
			getCurrentSlide();
			checkStatus();
			jQuery('.mm-finish-btn').removeClass('active');
			if( jQuery('.mm-page-'+current).hasClass('pass') ) {
				jQuery('.mm-survey-container').addClass('good');
				jQuery('.mm-survey').addClass('okay');
			}
			else {
				jQuery('.mm-survey-container').removeClass('good');
				jQuery('.mm-survey').removeClass('okay');
			}
			buttonConfig();
		});

	}

	function buildProgress(g) {

		if(g > 1){
			g = g - 1;
		}
		else if (g === 0) {
			g = 1;
		}
		g = g * 100;
		jQuery('.mm-survey-progress-bar').css({ 'width' : g+'%' });

	}

	function goToSlide(x) {

		return x;

	}

	function getCurrentSlide() {

		jQuery('.mm-survey-page').each(function() {

			var item;

			item = jQuery(this);

			if( jQuery(item).hasClass('active') ) {
				x = item.data('page');
			}
			else {
				
			}

			return x;

		});

	}

	function getButtons() {

		if(current === 0) {
			current = y;
		}
		if(current === count) {
			jQuery('.mm-next-btn').hide();
		}
		else if(current === 1) {
			jQuery('.mm-prev-btn').hide();
		}
		else {
			jQuery('.mm-next-btn').show();
			jQuery('.mm-prev-btn').show();
		}

	}

	jQuery('.mm-survey-q li input').each(function() {

		var item;
		item = jQuery(this);

		jQuery(item).on('click', function() {
			if( jQuery('input:checked').length > 0 ) {
		    	// console.log(item.val());
		    	jQuery('label').parent().removeClass('active');
		    	item.closest( 'li' ).addClass('active');
			}
			else {
				//
			}
		});

	});

	percent = (x/count) * 100;
	jQuery('.mm-survey-progress-bar').css({ 'width' : percent+'%' });

	function checkStatus() {
		jQuery('.mm-survery-content .mm-survey-item').on('click', function() {
			var item;
			item = jQuery(this);
			item.closest('.mm-survey-page').addClass('pass');
		});
	}

	function buildStatus() {
		jQuery('.mm-survery-content .mm-survey-item').on('click', function() {
			var item;
			item = jQuery(this);
			item.addClass('bingo');
			item.closest('.mm-survey-page').addClass('pass');
			jQuery('.mm-survey-container').addClass('good');
		});
	}

	function deliverStatus() {
		jQuery('.mm-survey-item').on('click', function() {
			if( jQuery('.mm-survey-container').hasClass('good') ){
				jQuery('.mm-survey').addClass('okay');
			}
			else {
				jQuery('.mm-survey').removeClass('okay');	
			}
			buttonConfig();
		});
	}

	function lastPage() {
		if( jQuery('.mm-next-btn').hasClass('cool') ) {
			alert('cool');
		}
	}

	function buttonConfig() {
		if( jQuery('.mm-survey').hasClass('okay') ) {
			jQuery('.mm-next-btn button').prop('disabled', false);
		}
		else {
			jQuery('.mm-next-btn button').prop('disabled', true);
		}
	}

	function submitData() {
		jQuery('.mm-finish-btn').on('click', function() {
			collectData();
			jQuery('.mm-survey-bottom').slideUp();
			jQuery('.mm-survey-results').slideDown();
		});
	}

	function collectData() {
		
		var map = {};
		var ax = ['0','red','mercedes','3.14','3'];
		var answer = '';
		var total = 0;
		var ttl = 0;
		var g;
		var c = 0;

		jQuery('.mm-survey-item input:checked').each(function(index, val) {
			var item;
			var data;
			var name;
			var n;

			item = jQuery(this);
			data = item.val();
			name = item.data('item');
			n = parseInt(data);
			total += n;

			map[name] = data;

		});

		jQuery('.mm-survey-results-container .mm-survey-results-list').html('');

		for (i = 1; i <= count; i++) {

			var t = {};
			var m = {};
			answer += map[i] + '<br>';
			
			if( map[i] === ax[i]) {
				g = map[i];
				p = 'correct';
				c = 1;
			}
			else {
				g = map[i];
				p = 'incorrect';
				c = 0;
			}

			jQuery('.mm-survey-results-list').append('<li class="mm-survey-results-item '+p+'"><span class="mm-item-number">'+i+'</span><span class="mm-item-info">'+g+' - '+p+'</span></li>');

			m[i] = c;
			ttl += m[i];

		}

		var results;
		results = ( ( ttl / count ) * 100 ).toFixed(0);

		jQuery('.mm-survey-results-score').html( results + '%' );

	}

	function goBack() {
		jQuery('.mm-back-btn').on('click', function() {
			jQuery('.mm-survey-bottom').slideDown();
			jQuery('.mm-survey-results').slideUp();
		});
	}