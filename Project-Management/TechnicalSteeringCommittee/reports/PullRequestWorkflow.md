Pull Requests
=============

## Workflow when work finished
1. Finish piece of work:
  * Code compiles (no warnings)
  * Unit tests added/upated
  * Documentation added/updated
  * All unit tests pass on your local machine
  * If any system tests could be affected, these should pass on local (your) machine
1. Open pull request (tests cross platform)
  * Link to issue
  * Write details of how to test changes
  * Pull request is annotated with build result
  * If required urgently, ask someone to test
  
## Workflow as tester
1. Check for [open pull requests](https://github.com/mantidproject/mantid/pulls?q=is%3Aopen+is%3Apr)
1. Pick a request that has a green tick and no one else assigned to it 
1. Open pull request and Click *assign yourself*
1. Test the changes on your local machine
1. If the issue passes:
  * Follow instructions at the bottom (including deleting the branch after the merge using the button on the page)
1. If the issue fails:
  * start a conversation on the pull request with the developer
  * add the **NeedsAttention** label
