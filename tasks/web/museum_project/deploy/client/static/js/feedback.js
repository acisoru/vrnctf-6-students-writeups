$("#feedback-form").submit(function(event) {
    event.preventDefault();

    const formData = {
        message_text: $("#message_text").val()
    };

    $.ajax({
        type: "POST",
        url: "http://localhost:80/api/feedback/send",
        data: JSON.stringify(formData),
        contentType: "application/json",
        dataType: "json",
        success: function(response_data) {
            $("#feedback-form").hide();
            $("#feedback-result").show();
            $("#feedback-content").text(response_data.message_text);
        },
        error: function() {
            alert("Произошла ошибка при отправке. Пожалуйста, попробуйте еще раз.");
        }
    });
});