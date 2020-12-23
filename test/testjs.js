var currentMenu;
var previousMenu;

function showMenuElement(menuName){
	if (currentMenu == menuName) return;
	previousMenu = currentMenu;
	currentMenu = menuName;
	document.getElementById(currentMenu).style.visibility = "visible";	  
	if (previousMenu != null) document.getElementById(previousMenu).style.visibility = "hidden";
}
