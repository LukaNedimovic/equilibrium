<h1> 📰 Equilibrium </h1>

Equilibrium is an <b> "Article Management System" </b>, created as a little project for "Scripting Languages" course (Faculty of Sciences, University of Novi Sad).

<h2> 📥 Installation </h2>
Installation is a very simple process:
<ol>
  <li>
    Clone the repository using: &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<code>git clone https://github.com/LukaNedimovic/equilibrium</code>
  </li>
  <li>
    Run the following to install dependencies: <code>pip install -r requirements.txt</code>
  </li>
</ol>

<h2> 🔥 Motivation </h2>

  <ul>
    <li> Research of machine learning models in creation of text-based recommendation systems. </li>
    <li> Creation of console application with "modern" GUI (multiple input boxes at the same time; selection / movement using arrow keys) </li>
  </ul>
  
<h2> ⚙️ Features </h2>

Equilibrium is a slightly-more-complex CRUD application - one can create an account, log in, create an article, delete it, interact with it (like / dislike / save), search for articles based on keywords, and get recommended an article similar to the one currently reading. 

Administrator account is already created and can be used to interact with platform completely - capable of deleting all articles, viewing keyword statistics and so on.

<h2> 🤖 Machine Learning Model </h2>

Main motivation behind creating such project was to get a bit more knowledge on how some machine learning concepts work - especially <b> embeddings </b>.

I have tried implementing 3 different models:
  <ol>
    <li> Article x Tag Model &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp - where premise is that similar articles share more of the similar tags </li>
    <li> Collaborative Filtering Model - where articles are suggested by trying to predict the rating based on other user's ratings </li>
    <li> <b> TF-IDF </b> &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp - standard method, combined with cosine similarity, which gave the best performance (being the simplest model out of these three)</li>
  </ol>

I wished to create a NN model that would eventually have a good performance, but noticed following:
  <ol>
    <li> I don't have sufficient data to create a good-working NN (for my current knowledge level, at the very least) </li>
    <li> It's better to use a simpler model if possible </li>
    <li> Hybrid model was possible and the most "modern" choice, but that would require a bit more time to implement and train </li>
  </ol>

TF-IDF performed extremely well on given dataset, was quick to train and easy to implement. My wish to learn more about some NN models were also fulfilled by creating these two "less good" models, so it balanced out meaningfully.

<h2> 🔍 What can be improved? </h2>

I believe that this project is good, especially being a "first semester" one. However, some meaningful changes can (and hopefully will) be made:
  <ol>
    <li> <b> Paths generation </b> &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp - a function should be implemented to generate the paths, or some other interesting workaround. It should be platform-agnostic, too. </li>
    <li> <b> Generalized version of prompt rendering </b> - it would be fun to create a module that renders these prompts dynamically, like miniature version of HTML. It could be also useful for programming newbies, who would then be able to create very nice console UIs. </li>
  </ol>
