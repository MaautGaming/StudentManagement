// $(document).on('keyup', "input[name='student_search']", function(){
// 	search_string = $( this ).val()
// 	parent = $( this ).parent()
// 	console.log(search_string)
// 	$('.searched_students').remove();
// 	if (search_string !== '') {
// 		$.ajax({
// 			url: '/students/' + search_string,
// 			type: 'GET',
// 			dataType: 'html',
// 			success: function( html ) {
// 				console.log(html);
// 				new_elements = $(html);
// 				parent.append( new_elements );
// 			}
// 		})
// 	};
// });

// $(document).on('keyup', "input[name='student_search']", function(){
// 	search_string = $( this ).val()
// 	console.log(search_string)
// 	$('.student_data').remove();
// 	if (search_string !== '') {
// 		$.ajax({
// 			url: '/students/' + search_string,
// 			type: 'GET',
// 			dataType: 'html',
// 			success: function( html ) {
// 				console.log(html);
// 				new_elements = $(html);
// 				$('.student_list').append( new_elements );
// 			}
// 		})
// 	}
// 	else{
// 		location.reload()
// 	}
// });

$(document).on('keyup', "input[name='student_search']", function(){
	search_string = $( this ).val()
	console.log(search_string)
	$('.student_data').remove();
	if (search_string !== '') {
		$.ajax({
			url: '/students/' + search_string,
			type: 'GET',
			dataType: 'html',
			success: function( html ) {
				console.log(html);
				new_elements = $(html);
				$('.student_list').append( new_elements );
			}
		})
	}
	else{
		location.reload()
	}
});