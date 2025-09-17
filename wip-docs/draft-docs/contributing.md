---
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Copy of Contributing

## ⭐ CONTRIBUTING

## Contributing to Lightning Bounties

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the Table of Contents for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
>
> * Star the project
> * Tweet about it
> * Refer this project in your project's readme
> * Mention the project at local meetups and tell your friends/colleagues

### Table of Contents

* I Have a Question
* I Want To Contribute
  * Reporting Bugs
  * Suggesting Enhancements
  * Your First Code Contribution
  * Improving The Documentation
* Styleguides
  * Commit Messages
* Join The Project Team

### I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://github.com/Lightning-Bounties/docs).

Before you ask a question, it is best to search for existing [Issues](https://github.com/MIT-Bitcoin-2024/lightning-bounty/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

* Open an [Issue](https://github.com/MIT-Bitcoin-2024/lightning-bounty/issues/new).
* Provide as much context as you can about what you're running into.
* Provide project and platform versions (python, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

### I Want To Contribute

> **Legal Notice**
>
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

#### Reporting Bugs

**Before Submitting a Bug Report**

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

* Make sure that you are using the latest version.
* Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://github.com/Lightning-Bounties/docs). If you are looking for support, you might want to check this section).
* To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/MIT-Bitcoin-2024/lightning-bountyissues?q=label%3Abug).
* Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
* Collect information about the bug:
  * Stack trace (Traceback)
  * OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  * Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
  * Possibly your input and the output
  * Can you reliably reproduce the issue? And can you also reproduce it with older versions?

**How Do I Submit a Good Bug Report?**

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to .

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

* Open an [Issue](https://github.com/MIT-Bitcoin-2024/lightning-bounty/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
* Explain the behavior you would expect and the actual behavior.
* Please provide as much context as possible and describe the _reproduction steps_ that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
* Provide the information you collected in the previous section.

Once it's filed:

* The project team will label the issue accordingly.
* A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
* If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be implemented by someone.

#### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Lightning Bounties, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

**Before Submitting an Enhancement**

* Make sure that you are using the latest version.
* Read the [documentation](https://github.com/Lightning-Bounties/docs) carefully and find out if the functionality is already covered, maybe by an individual configuration.
* Perform a [search](https://github.com/MIT-Bitcoin-2024/lightning-bounty/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
* Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

**How Do I Submit a Good Enhancement Suggestion?**

Enhancement suggestions are tracked as [GitHub issues](https://github.com/MIT-Bitcoin-2024/lightning-bounty/issues).

* Use a **clear and descriptive title** for the issue to identify the suggestion.
* Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
* You may want to **include screenshots and animated GIFs** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **Explain why this enhancement would be useful** to most Lightning Bounties users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

#### Your First Code Contribution

To make your first code contribution, follow these steps:

1. Fork the Repository and Clone it
   * Fork the repository on GitHub.
   * Clone the forked repository to your local machine.
2. Modify the Code
   * Open the `src/main.py` file and make the desired changes to reflect your modifications.
3. Generate a Lightning Invoice
   * Generate a lightning invoice for the payment.
   * Copy the invoice string into the `reward.txt` file.
4. Commit and Submit a Pull Request
   * Add and commit your changes to the local repository.
   * Submit a pull request to the base repository.
5. Pay the Invoice
   * A GitHub action will be triggered to request a "dust" payment from you (the contributor) to the base repository (the owner).
   * Choose the action that says "Please pay the invoice: lnbc10n1..." (not the one that says "Extracted values:...").
   * Wait for the payment confirmation.
   * Once the payment is confirmed, you'll receive a message saying "Thank you for your payment!"
6. Request a Reviewer
   * Ask for a reviewer to review your pull request.
   * Choose either Enrique or Will for this test.
7. Review and Analysis
   * After a few seconds, a new action will run.
   * It will first say "Payment has been received, sit tight, running openai query."
   * Approximately 30 seconds later, it will return with a summary of your changes and a security vulnerability analysis.
8. Merging the Pull Request
   * We'll keep an eye out for your pull request and attempt to merge it for you. As a contributor, you don't have the power to merge it yourself.

Alternatively, if you prefer to replicate our work in your own repository:

* Copy the contents of the `.github/` directory into your repository.
* Modify the `main.py` file accordingly.
* Set up the following secrets in your repository settings:
  * `OPENAI_API_KEY`
  * `PAY_INVOICE_KEY` (admin key for LNBits)
  * `WALLET_API_KEY` (invoice/read key for LNBits)
  * `WALLET_BASE_URL` (URL for your LNBits instance)

#### Improving The Documentation

If you want to improve the documentation, please follow the same process as described in the "Your First Code Contribution" section, but focus on updating the documentation files instead of the code.

### Styleguides

#### Commit Messages

When writing commit messages, please follow these guidelines:

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Join The Project Team

If you're interested in joining the project team, please contact us at founders@lightningbounties.com.

### Attribution

This guide is based on the **contributing-gen**. [Make your own](https://github.com/bttger/contributing-gen)!

***

### Disclaimer

!!! warning "Beta Version" This project is currently in beta and under active development. The testing process described in this document may change frequently as we make updates and improvements.

If you have any questions or would like to discuss potential contributions, please email us at founders@lightningbounties.com.
