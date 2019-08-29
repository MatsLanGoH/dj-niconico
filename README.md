# NICONICO

- Description to be updated.

Operation | Url | Action
--- | --- | ---
GET | /api/moods/ | Shows moods for logged in user
GET | /api/moods/{id} / Shows mood details for logged in user
GET | /api/teams/ | Shows teams for logged in user
GET | /api/teams/{UUID}/moods/ | Shows moodboard for team if logged in user is member or owner of team
GET | /api/teams/{UUID}/members/ | Shows team members if logged in user is member or owner
PUT | /api/teams/{UUID}/members/{member_id}/ | Update member status (approve/reject/delete if owner), (delete if self) 

