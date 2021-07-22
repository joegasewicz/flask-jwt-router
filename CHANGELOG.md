# Changelog

### Changed

**Releases 0.2.0** - 2021-07-21
- 🎁 Remove testing logic from library's `Routing` & `Entity` classes  [Issue #219](https://github.com/joegasewicz/flask-jwt-router/issues/219)
- 🎁 Testing mixin for Google class  [Issue #220](https://github.com/joegasewicz/flask-jwt-router/issues/220)
- 🪲 Bug fixes for 0.2.0 release Fixes [Issue #225](https://github.com/joegasewicz/flask-jwt-router/issues/225)

**Releases 0.1.9** - 2021-03-16
- 🎁 Allow for multiple tablenames for Google OAuth  [Issue #206](https://github.com/joegasewicz/flask-jwt-router/issues/206)

**Releases 0.1.8** - 2021-03-16
- 📝 Outdated docstring - nice easy fix for a beginner developer! [Issue #192](https://github.com/joegasewicz/flask-jwt-router/issues/192)
- 🎁 Bump cryptography from 3.3.1 to 3.3.2 #197
- 🎁 Multiple redirect URI's for Google OAuth #203 [Issue #203](https://github.com/joegasewicz/flask-jwt-router/issues/203)

**Releases 0.1.7** - 2021-01-27
- 🎁 Test utils for OAuth users should handle multiple user states. [Issue #188](https://github.com/joegasewicz/flask-jwt-router/pull/188)

**Releases 0.1.6** - 2021-01-27
- 🎁 Google test utility method can be scoped between tests. [Issue #185](https://github.com/joegasewicz/flask-jwt-router/issues/185)

**Releases 0.1.5** - 2021-01-26
- 🎁 Added extra test in  [_routing.py line 174](https://github.com/joegasewicz/flask-jwt-router/blob/6ee5bcfb772b6cb66a5c621cf466014b94eaf635/flask_jwt_router/_routing.py#L174) for better check for X-Auth-Token headers.
- 🎁 Provide a utility method for testing & mocking OAuth headers. [Issue #183](https://github.com/joegasewicz/flask-jwt-router/issues/183)

**Releases 0.0.29 to 0.1.4** -

- README.md references `user` but example table is `users`. [Issue #154](https://github.com/joegasewicz/flask-jwt-router/issues/154)
- 🎁 Add OAuth 2.0 & compatibility with react-google-oauth2 npm pkg. [Issue #158](https://github.com/joegasewicz/flask-jwt-router/issues/158)
- 📝 Fix docs. [Issue #162](https://github.com/joegasewicz/flask-jwt-router/issues/162)
- 🪲 Fix url is mutated. [Issue #169](https://github.com/joegasewicz/flask-jwt-router/issues/169)
- 🪲 Entity key state gets stale between requests. [Issue #171](https://github.com/joegasewicz/flask-jwt-router/issues/171)
- 🪲 Table name form oauth request is stale. [Issue #173](https://github.com/joegasewicz/flask-jwt-router/issues/173)
- 🪲 Clean up entity state before auth routing . [Issue #175](https://github.com/joegasewicz/flask-jwt-router/issues/175)
- 🪲 Return 401 status is oauth returns none. [Issue #177](https://github.com/joegasewicz/flask-jwt-router/issues/177)
- 🪲 PyJWT 2.0 causes Breaking change. [Issue #179](https://github.com/joegasewicz/flask-jwt-router/issues/179)

**Release 0.0.28** -

- 🎁 Created custom error for `update_token` method called on non existent token [Issue #151](https://github.com/joegasewicz/flask-jwt-router/issues/151)
- 📝 Updated `Authenticate`'s `update_token` method's doc string with entity_id kwarg. [Issue #150](https://github.com/joegasewicz/flask-jwt-router/issues/150) 
- 📝 README.md references `user` but example table is `users` [Issue #154](https://github.com/joegasewicz/flask-jwt-router/issues/154)

**Release 0.0.27** - 2020-09-14

- 🪲 Secret Key now must be set [Issue #137](https://github.com/joegasewicz/flask-jwt-router/issues/137)
- 🪲 Fixes ModuleNotFoundError: No module named 'dateutil' [Issue #138](https://github.com/joegasewicz/flask-jwt-router/issues/138)
- 🎁 Removes strategy design pattern from project [Issue #141](https://github.com/joegasewicz/flask-jwt-router/issues/141)
- 🎁 Renamed extensions to Config [Issue #143](https://github.com/joegasewicz/flask-jwt-router/issues/143)
- 🎁 Added token expire duration option [Issue #44](https://github.com/joegasewicz/flask-jwt-router/issues/44)

**Release 0.0.26** - 2019-12-11

- 🪲 Preflight OPTIONS bug fix [Issue #125](https://github.com/joegasewicz/Flask-JWT-Router/issues/125)

**Release 0.0.25** - 2019-12-10

- 🎁 Replaced the the `entity_type` kwarg to `table_name` in the public method `register_entity` [Issue #111](https://github.com/joegasewicz/Flask-JWT-Router/issues/111)
- 🎁 Renamed the `update_entity` public method to be called `update_token` [Issue #114](https://github.com/joegasewicz/Flask-JWT-Router/issues/114)
- 🎁 Renamed the `register_entity` public method to be called `create_token` [Issue #113](https://github.com/joegasewicz/Flask-JWT-Router/issues/113)
- 🎁 Add Models to JWTRoutes class & init_app method [Issue #119](https://github.com/joegasewicz/Flask-JWT-Router/issues/119)

## Unreleased

