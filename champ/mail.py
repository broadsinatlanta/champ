def sendFeedback(feedback, email, password):
    """
    Send email to admin using smtpbplib, containing form data.

    Assumes input is Feedback object (feedback form data).
    """

    import smtplib as s

    # Start (Gmail) server
    server = s.SMTP("smtp.gmail.com", 587)

    # Security encryption
    server.starttls()

    # Login to email
    server.login(email, password)

    message = f"""
    From: {feedback.name}\n
    Reply (To) Email: {feedback.email}\n
    They liked: {feedback.positive}\n
    They would improve: {feedback.negative}\n
    Overall Experience: {feedback.sentiment}\n
    ----------------------------------------
    Message:\n
    {feedback.message}
    """

    server.sendmail(email, email, message)

    server.quit()
    print("Server quit.")
