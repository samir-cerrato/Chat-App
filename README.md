# Chat-App
Create a simple chat app

Your chat app will function as a group chat. All chat clients first
connect to the chat server. When any chat client wants to send a message to the other chat clients,
it sends the message over its connection with the chat server, which then sends it to each of the
other chat clients. Thus, whenever one client sends a message, all client receive it.

•Chat client. You will see that the chat client is multi-threaded with a write sock function
called in one thread and a read sock function called in the other. These sockets write and
read data respectively from the chat server. These are the only functions you need to fill out.

– In the write sock function you will continuously read data from the command line
(i.e., user input), put your protocol header on it, and write it to the chat server. Your
protocol header should comprise several fields, including at least the length (in bytes)
of the data. You will need some way of determining when the header terminates, and
when the data being sent (payload) begins.

– In the read sock function you will continuously read data from the socket with the
server, parse the protocol header that the server put on the data it sent, determine
how much data to read, read until you get the expected amount of data, and display it
(print) to the screen. When you print to the screen, you should format the display so
that the name of the user who sent the data comes first, followed by a colon, followed
by the data, as in, “user: data”.

•Chat server. The chat server spawns a thread to serve each client. The chat server,
however, when serving a client in one thread, may need to write data to clients in other
threads, and so will now need to have access to all client sockets regardless of which thread
is currently being run. To handle this, a list of sockets will be maintained, along with their
associated IDs: this has already been implemented for you. What you need to fill out are
the following functions.

– In the serve user function you will use the read data function to continuously read
data from the socket (i.e., chat client) being served in that thread. Whenever you
have read a complete message you will send it to all other clients using the send data
function. Note: you should not access the chat list variable in this function.

– In the read data function you will read from the socket passed to the function, check
whether a full message has been received, and when it has, return that message so it
can be sent to the other clients. You will want to check whether an empty string has
been read from the socket, indicating that the client has left.

– In the send data function you will loop through all of the available connections and
send the message to every other client, excepting the original sending client.

– In the cleanup function you will close the socket being served in the thread as well as
remove the connection from the list of connections available.
