# crud_fastapi_2

FastAPI for CRUD API creation.

## To Do

- [x] How to take only one parameter even the same is provided multiple time (No vuln for that because the control must be on how we use the parameter, so...)
- [x] Run Redis with Docker and test the logout functionality (docker run --name redis -p 6379:6379 -d redis)
- [ ] Add verification email to user
- [ ] Change verification date if yes
- [ ] Add Roles check on books endpoints
  - [x] Get All Books (Admin can get all books. User can get all not deleted book he created)
  - [ ] Publish A Book (Admin or user. Admin can update a book for a user)
  - [x] Get All Published Books (Admin can get all published books. User can get all books he published)
  - [x] Unpublish A Book (Admin or user. Admin can update a book for a user)
  - [x] Get all unpublished Books (Admin can get all unpublished books. User can get all books he unpublished)
  - [x] Delete A Book (Admin or user. Admin can update a book for a user)
  - [x] Get Deleted Books (Admin only)
  - [x] Get A Book (Admin or user)
  - [x] Update Book (Admin or user. Admin can update a book for a user)
  - [x] Hard Delete Book (Admin only)
- [x] Get all users (Admin only)
- [x] Get one user (Admin only)