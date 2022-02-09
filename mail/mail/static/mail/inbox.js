document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#content-view').style.display = 'none';
  document.querySelector('#compose-form').onsubmit =  function() {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
      })
    .then(response => response.json())
    .then(result => {

      load_mailbox('sent');
    });
    
    return false;
  }
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email("","",""));

  try { if (document.querySelector('h3').innerHTML != "Sent")
    load_mailbox('inbox');
  // By default, load the inbox
  }

  catch (TypeError)
  {console.log("<h3> is not found.")}
});

function compose_email(recipientsI, subjectI, bodyI) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#content-view').style.display = 'none';
  document.querySelector('#get-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipientsI;
  document.querySelector('#compose-subject').value = subjectI;
  document.querySelector('#compose-body').value = bodyI;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'none';
  document.querySelector('#get-view').style.display = 'block';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 class="h3-mailbox">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`; 

    var text = "";
    if (mailbox == 'inbox')
    {
     fetch ('/emails/inbox')
    .then( response => response.json())
    .then( data => {

        document.querySelector('.table-inbox').innerHTML = "";
        if (data.length == 0) {
          document.querySelector('.table-inbox').innerHTML = `<strong>Your inbox seems empty.</strong>`
        }
        for (var i = 0;i < data.length; i++)
        {
          var read = (data[i].read) ? "read" : "not-read";
          let tr = document.createElement('tr');
          tr.classList.add('in-inbox', read);
          
          let td0 = document.createElement('td');
          td0.className = 'td-inbox';

          let button = document.createElement('button');
          button.className = 'in-button';
          button.dataset.id = data[i].id;
          button.innerHTML = data[i].sender;

          let x = data[i].id
          let tempsender = data[i].sender
          let tempsubject = data[i].subject
          let tempbody = data[i].body
          let temptimestamp = data[i].timestamp

          button.addEventListener('click', () => {
            document.querySelector('#content-view').style.display = 'block';
            document.querySelector('#get-view').style.display = 'none';

            let content = document.querySelector('#content-view');
            content.innerHTML = "";
            fetch (`/emails/${x}`)
            .then (response => response.json())
            .then (data0 => {

              let email = `<b>${data0[0].subject}</b><br>`;
              email += `${data0[0].sender}<br>${data[0].timestamp}<br>`;
              email += `<p style="white-space: pre-wrap;">${data0[0].body}</p><br>`;

              let emaildiv = document.createElement('div')
              emaildiv.innerHTML = email;
              content.append(emaildiv);
              });
            
            
            let inboxbutton = document.createElement('button')
            inboxbutton.innerHTML = "<-";
            inboxbutton.addEventListener('click', () => {
                tr.classList.remove('not-read');
                tr.classList.add('read');
                document.querySelector('#content-view').style.display = 'none';
                document.querySelector('#get-view').style.display = 'block';

                fetch(`/emails/${x}`, {
                  method : 'PUT',
                  body: JSON.stringify({
                    read: true
                  })
                }) 
              });

              content.appendChild(inboxbutton);

              let unread = document.createElement('button');
              unread.innerHTML = 'Unread';
              unread.addEventListener('click', () => {
                tr.classList.remove('read');
                tr.classList.add('not-read');
                document.querySelector('#content-view').style.display = 'none';
                document.querySelector('#get-view').style.display = 'block';

                fetch(`/emails/${x}`, {
                  method : 'PUT',
                  body: JSON.stringify({
                    read: false
                  })
                })
              });
              content.append(unread);

              let archivebutton = document.createElement('button');
              archivebutton.innerHTML = "Archive";
              archivebutton.addEventListener('click', () => {

                fetch(`/emails/${x}`, {
                  method : 'PUT',
                  body: JSON.stringify({
                    archived: true
                  })
                })
                document.location.reload(true)
               
              });
              content.append(archivebutton);

              let replybutton = document.createElement('button');
              replybutton.innerHTML = "Reply";
              replybutton.addEventListener('click', () => {
                

                let newtempsubject = (tempsubject.slice(0,3) == "Re:") ? tempsubject : `Re: ${tempsubject}`
                compose_email(tempsender, newtempsubject, `On ${temptimestamp} ${tempsender} wrote: \n${tempbody}\n----------------------------------------------\n`)
              });
              content.append(replybutton)
            });
            td0.appendChild(button);
            tr.appendChild(td0);
            
            let td1 = document.createElement('td');
            td1.className = 'td-inbox';
            td1.innerHTML = data[i].subject;
            tr.appendChild(td1);

            let td2 = document.createElement('td');
            td2.className = 'td-inbox';
            td2.innerHTML = data[i].timestamp;
            tr.appendChild(td2);
            document.querySelector('.table-inbox').append(tr);
          
         }
      });
    }
    else if (mailbox == 'sent')
    {
    fetch ('/emails/sent')
    .then( response => response.json())
    .then( data => {

        document.querySelector('.table-inbox').innerHTML = "";
        if (data.length == 0)  {
          document.querySelector('.table-inbox').innerHTML = `<strong>Sent mailbox seems empty. Send an email to see it here.</strong>`
        }
        for (var i = 0; i < data.length; i++)
        {
          var read = (data[i].read) ? "read" : "not-read";
          let tr = document.createElement('tr');
          tr.classList.add('in-inbox', read);

          let td0 = document.createElement('td');
          td0.className = 'td-inbox';

          let button = document.createElement('button');
          button.className = 'in-button';
          button.innerHTML = data[i].sender;

          let x = data[i].id
          let tempsender = data[i].sender
          let tempsubject = data[i].subject
          let tempbody = data[i].body
          let temptimestamp = data[i].timestamp
          button.addEventListener('click', () => {
            document.querySelector('#content-view').style.display = 'block';
            document.querySelector('#get-view').style.display = 'none';


            let content = document.querySelector('#content-view');
            content.innerHTML = "";
            fetch (`/emails/${x}`)
            .then (response => response.json())
            .then (data0 => {

              let email = `<b>${data0[0].subject}</b><br>`;
              email += `${data0[0].sender}<br>${data[0].timestamp}<br>`;
              email += `<p style="white-space: pre-wrap;">${data0[0].body}</p><br>`;

              let emaildiv = document.createElement('div')
              emaildiv.innerHTML = email;
              content.append(emaildiv);
              });
            
            
            let sentbutton = document.createElement('button')
            sentbutton.innerHTML = "<-";
            sentbutton.addEventListener('click', () => {
                tr.classList.remove('not-read');
                tr.classList.add('read');
                document.querySelector('#content-view').style.display = 'none';
                document.querySelector('#get-view').style.display = 'block';

                fetch(`/emails/${x}`, {
                  method : 'PUT',
                  body: JSON.stringify({
                    read: true
                  })
                }) 
              });

              content.appendChild(sentbutton);

              let unread = document.createElement('button');
              unread.innerHTML = 'Unread';
              unread.addEventListener('click', () => {
                tr.classList.remove('read');
                tr.classList.add('not-read');
                document.querySelector('#content-view').style.display = 'none';
                document.querySelector('#get-view').style.display = 'block';

                fetch(`/emails/${x}`, {
                  method : 'PUT',
                  body: JSON.stringify({
                    read: false
                  })
                })
              });
              content.append(unread);

              let replybutton = document.createElement('button');
              replybutton.innerHTML = "Reply";
              replybutton.addEventListener('click', () => {
                

                let newtempsubject = (tempsubject.slice(0,3) == "Re:") ? tempsubject : `Re: ${tempsubject}`
                compose_email(tempsender, newtempsubject, `On ${temptimestamp} ${tempsender} wrote: \n${tempbody}\n----------------------------------------------\n`)
              });
              content.append(replybutton)
            });

          td0.appendChild(button);
          tr.appendChild(td0);

          let td1 = document.createElement('td');
          td1.className = 'td-inbox';
          td1.innerHTML = data[i].subject;
          tr.appendChild(td1);

          let td2 = document.createElement('td');
          td2.className = 'td-inbox';
          td2.innerHTML = data[i].timestamp;
          tr.appendChild(td2);
          document.querySelector('.table-inbox').append(tr);
        }


    });
    } 
    else if (mailbox == 'archive')
    {
      fetch ('/emails/archive')
    .then( response => response.json())
    .then( data => {
        document.querySelector('.table-inbox').innerHTML = "";
        if (data.length == 0)
        {
          document.querySelector('.table-inbox').innerHTML = `<strong>Archive mailbox seems empty. Archive an email to see it here.</strong>`
        }
        for (var i = 0; i < data.length; i++)
        {
          var read = (data[i].read) ? "read" : "not-read";
          let tr = document.createElement('tr');
          tr.classList.add('in-inbox', read);
          
          let td0 = document.createElement('td');
          td0.className = 'td-inbox';

          let button = document.createElement('button');
          button.className = 'in-button';  /*not sure what this is doing here*/ 
          button.innerHTML = data[i].sender;

          let x = data[i].id
          let tempsender = data[i].sender
          let tempsubject = data[i].subject
          let tempbody = data[i].body
          let temptimestamp = data[i].timestamp
          button.addEventListener('click', () => {
            document.querySelector('#content-view').style.display = 'block';
            document.querySelector('#get-view').style.display = 'none';


            let content = document.querySelector('#content-view');
            content.innerHTML = "";
            fetch (`/emails/${x}`)
            .then (response => response.json())
            .then (data0 => {

              let email = `<b>${data0[0].subject}</b><br>`;
              email += `${data0[0].sender}<br>${data[0].timestamp}<br>`;
              email += `<p style="white-space: pre-wrap;">${data0[0].body}</p><br>`;

              let emaildiv = document.createElement('div')
              emaildiv.innerHTML = email;
              content.append(emaildiv);
              });
            
            
            let archiveB = document.createElement('button')
            archiveB.innerHTML = "<-";
            archiveB.addEventListener('click', () => {
                tr.classList.remove('not-read');
                tr.classList.add('read');
                document.querySelector('#content-view').style.display = 'none';
                document.querySelector('#get-view').style.display = 'block';

                fetch(`/emails/${x}`, {
                  method : 'PUT',
                  body: JSON.stringify({
                    read: true
                  })
                }) 
              });

              content.appendChild(archiveB);

              let unread = document.createElement('button');
              unread.innerHTML = 'Unread';
              unread.addEventListener('click', () => {
                tr.classList.remove('read');
                tr.classList.add('not-read');
                document.querySelector('#content-view').style.display = 'none';
                document.querySelector('#get-view').style.display = 'block';

                fetch(`/emails/${x}`, {
                  method : 'PUT',
                  body: JSON.stringify({
                    read: false
                  })
                })
              });
              content.append(unread);

              let unarchivebutton = document.createElement('button');
              unarchivebutton.innerHTML = "Unarchive";
              unarchivebutton.addEventListener('click', () => {

                fetch(`/emails/${x}`, {
                  method : 'PUT',
                  body: JSON.stringify({
                    archived: false
                  })
                })
                document.location.reload(true)
               
              });
              content.append(unarchivebutton);

              let replybutton = document.createElement('button');
              replybutton.innerHTML = "Reply";
              replybutton.addEventListener('click', () => {
                

                let newtempsubject = (tempsubject.slice(0,3) == "Re:") ? tempsubject : `Re: ${tempsubject}`
                compose_email(tempsender, newtempsubject, `On ${temptimestamp} ${tempsender} wrote: \n${tempbody}\n----------------------------------------------\n`)
              });
              content.append(replybutton)
          });

          td0.appendChild(button);
          tr.appendChild(td0);

          let td1 = document.createElement('td');
          td1.className = 'td-inbox';
          td1.innerHTML = data[i].subject;
          tr.appendChild(td1);

          let td2 = document.createElement('td');
          td2.className = 'td-inbox';
          td2.innerHTML = data[i].timestamp;
          tr.appendChild(td2);
          document.querySelector('.table-inbox').append(tr);
        }
    });
    }
}