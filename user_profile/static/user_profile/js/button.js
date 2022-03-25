$(document).on('click', 'button', function(){
	var id = $(this).attr('id');
	var name = $(this).attr('name')
	console.log("Clicked", id)
	if (confirm("Are you sure you want to delete it.")) {
		if (name === "delete_course") {
			$.ajax({
				url: '/course/delete/'+id,
				success: function() {
					location.reload();	
					}
			});
		}
		else {
			$.ajax({
				url: '/subject/'+id,
				success: function() {
						location.reload();	
					}
			});
		};
	};
});

$(document).on('click', '#add_more', function(){
        cloneMore('div.table:last', 'subject');
});