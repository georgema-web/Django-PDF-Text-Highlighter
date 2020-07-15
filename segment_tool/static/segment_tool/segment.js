
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
	    const cookies = document.cookie.split(';');
	    for (let i = 0; i < cookies.length; i++) {
	        const cookie = cookies[i].trim();
	        // Does this cookie string begin with the name we want?
	        if (cookie.substring(0, name.length + 1) === (name + '=')) {
	            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	            break;
	        }
	    }
	}
	return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function increaseKernel (img_id){

	const csrftoken = getCookie('csrftoken');
	
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
	
	$.ajax({
		url:'increase_kernel', 
		data: {
		'img_id':img_id
		}, 
		type: 'POST',
		error: function(xhr){			
		    alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
		},
		success: function(){
			location.reload();
		},
		timeout: 3000
	})
	}
function decreaseKernel (img_id){
	const csrftoken = getCookie('csrftoken');
	
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
	
	$.ajax({
		url:'decrease_kernel', 
		data: {
		'img_id':img_id
		}, 
		type: 'POST',
		error: function(xhr){			
		    alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
		},
		success: function(){
			location.reload();
		},
		timeout: 3000
	})
}






