document.addEventListener('DOMContentLoaded', function() {

    // Like Post
    document.querySelectorAll('#like_post').forEach(post => {
        post.onclick = function() {
            const liked_post = this.dataset.like;
            like_post(liked_post);
        };
    });

    // Unlike Post
    document.querySelectorAll('#unlike_post').forEach(post => {
        post.onclick = function() {
            const unliked_post = this.dataset.unlike;
            unlike_post(unliked_post);
        };
    });

    // Edit Post
    document.querySelectorAll('#edit_post').forEach(post => {
        post.onclick = function() {
            const edited_post = this.dataset.edit;
            edit_post(edited_post);
        };
    });   
})


function like_post(liked_post) {

    like_button = event.target

    fetch(`/like/${liked_post}`, {
      method: 'PUT',
      body: JSON.stringify({
          liked: true
      })
    })
    .then(response => response.json())
    .then(post => { 
        like_button.parentElement.innerHTML = `
        <div>
            <h2 style="color: red; display: inline;">&#9829;</h2>
            <h4 id="like_count" style="font-size: 28px; display: inline;">${post.post_reactions.length}</h4>
            <button style="display: inline; color: white;" class="btn btn-light btn-sm" id="unlike_post" data-unlike="${liked_post}" type="submit" value="unlike">Unlike</button><br>
        </div>
        `
        // Listen again for the newly added unlike_post element
        document.querySelectorAll('#unlike_post').forEach(post => {
            post.onclick = function() {
                const unliked_post = this.dataset.unlike;
                unlike_post(unliked_post);
            };
        });
    })
}



function unlike_post(unliked_post) {

    unlike_button = event.target

    fetch(`/unlike/${unliked_post}`, {
      method: 'PUT',
      body: JSON.stringify({
          unliked: true
      })
    })
    .then(response => response.json())
    .then(post => {
        unlike_button.parentElement.innerHTML = `
        <div>
            <h2 style="color: grey; display: inline;">&#9829;</h2>
            <h4 id="like_count" style="font-size: 28px; display: inline;">${post.post_reactions.length}</h4>
            <button style="display: inline; color: white;" class="btn btn-light btn-sm" id="like_post" data-like="${unliked_post}" type="submit" value="Like">Like</button><br>
        </div>
        `
        // Listen again for the newly added like_post element
        document.querySelectorAll('#like_post').forEach(post => {
            post.onclick = function() {
                const liked_post = this.dataset.like;
                like_post(liked_post);
            };
        });
    });
}



function edit_post(edited_post) {
    
    edit_button = event.target 

    document.querySelectorAll('#submitted').forEach(submited_post => {
        if (submited_post.dataset.submitted == edited_post) {
            edit_button.parentElement.innerHTML = `
            <form id="edit_form" method="put" style="margin-bottom: 25px; margin-top: 25px;">
                <div class="form-row justify-content-center"> 
                    <div class="col-8">
                        <textarea id="post-body" class="form-control" rows="8" name="post_body" type="textarea" maxlength="240">${submited_post.innerHTML}</textarea>
                    </div>
                </div>
               <button style="margin-top: 25px; color: white;" id="edit" value="Save" data-edit="${edited_post}" type="submit" class="btn btn-light">Save</input>
            </form>
            `
        }
    });
 
    document.querySelector('#edit').onclick = function() {
        let postbody = document.querySelector('#post-body').value;
        
        fetch(`edit/${edited_post}`, {
          method: 'PUT',
          body: JSON.stringify({
              post_body: postbody,
          })
        })
        .then(response => response.json())
        .then(post => {
            document.querySelector('#edit_form').parentElement.innerHTML = `
            <button style="display: inline; color: white; margin-top: -75px;" class="btn btn-light btn-sm" id="edit_post" data-edit="${edited_post}" type="submit" value="Edit">Edit Post</button><br>
            <h3 id="submitted" data-submitted="${edited_post}">${post.post_body}</h3>
            `
            // Listen for newly added edit_post button
            document.querySelectorAll('#edit_post').forEach(post => {
                post.onclick = function() {
                    const edited_post = this.dataset.edit;
                    edit_post(edited_post);
                };
            });
        }); 
        return false;
    }
}
