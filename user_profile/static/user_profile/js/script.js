$(document).ready(function() {
	$(".nav-link").each(function(){
		text = $(this).text()
		if (text.includes(document.title)){
			$(this).addClass('active')
		};
	});
});