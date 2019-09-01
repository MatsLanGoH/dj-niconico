# NICONICO

- [x] Single-user moods
- [ ] User account page

  - Change name
  - Delete account
  - etc.
 
- [ ] Teams

  - Create teams
  - Get shareable links to invite other users
  - Join link 
    (if there is a team for the pk
     and the user is not owner
     and the user is not a member
     let them join)
  - Approve new users (status kept in membership)
  - API only
  - Owner transfer?
  - Confirmation prompts front
  - Decision chart who can do what?
  - If team manager: see approved/unapproved memberships for team
  - If member: see moods for team
  
- [ ] Memberships

  - 
  
- [ ] Moods through memberships

  - Get most recent per day or unset
  - 

Operation | Url | Action
--- | --- | ---
GET | /api/moods/ | Shows moods for logged in user
GET | /api/moods/{id} / Shows mood details for logged in user
GET | /api/teams/ | Shows teams for logged in user
GET | /api/teams/{UUID}/moods/ | Shows moodboard for team if logged in user is member or owner of team
GET | /api/teams/{UUID}/members/ | Shows team members if logged in user is member or owner
PUT | /api/teams/{UUID}/members/{member_id}/ | Update member status (approve/reject/delete if owner), (delete if self) 

