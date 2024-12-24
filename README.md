# crud_fastapi_2

FastAPI for CRUD API creation.

## To Do

- [x] How to take only one parameter even the same is provided multiple time (No vuln for that because the control must be on how we use the parameter, so...)
- [x] Run Redis with Docker and test the logout functionality (docker run --name redis -p 6379:6379 -d redis)
- [ ] Add verification email to user
- [ ] Change verification date if yes
- [ ] Add Roles check on books endpoints
  - [ ] Get All Books (Admin only)
  - [ ] Create A Book (Admin or user. Admin can update a book for a user)
  - [ ] Publish A Book (Admin or user. Admin can update a book for a user)
  - [ ] Get All Published Books (Admin or user. Admin can update a book for a user)
  - [ ] Unpublish A Book (Admin or user. Admin can update a book for a user)
  - [ ] Get Unpublished Books (Admin or user. Admin can update a book for a user)
  - [ ] Delete A Book (Admin or user. Admin can update a book for a user)
  - [ ] Get Deleted Books (Admin or user. Admin can update a book for a user)
  - [ ] Get A Book (Admin or user)
  - [ ] Update Book (Admin or user. Admin can update a book for a user)
  - [ ] Hard Delete Book (Admin only)
- [ ] Get all users (Admin only)