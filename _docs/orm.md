# ORM
=======

- Introduction
- Define
- Create
  - Create single model
  - Create multiple models
- Update
  - Update single model
  - Update multiple models
- Save
- Delete
  - Delete single model
  - Delete multiple models
- Retrieving Modles
  - Aggregates

----

## Introduction
the orm which implement ActiveRecord

```
  -- create the table
  
  create table users (
    id int auto_increment primary key ,
    name varchar(32) not null default '',
    age int not null default 20
  );
```

## Define

```
  class User(Model):
    pass
```

User would be add column named `created_at`, `updated_at`, `id` auto. And `created_at`, `updated_at` are datetime type, id is a integer auto increament

if you won't create `created_at` and `updated_at`, you can set `__timestamp__` is False in User. Just like this:

```
  class User(Model):
    __timestamp__ = False

```

## Create
### Create single model
```
  User.create(name='jim', age=25)
```

### Create multiple models
```
  User.create_all(
    dict(name='jim', age=25),
    dict(name='jon', age=35),
    dict(name='lily', age=20),
  )
```

## Update
### Update single model
```
  u = User.find(1)   # find the user which id = 1
  u.update(name="lily", age=20)
```

### Update multiple models
```
  User.update_all(name='lily', age=20) # udpate all users set name = 'lily' and age = 20
```

## Save
```
  u = User(name='jim', age=25)
  u.save() # will be create a model

  u = User.find(1)
  u.name = 'jon'
  u.age = 30
  u.save() # will be update
```


## Delete
### Delete single model
```
  u = User.find(1)
  u.delete()
```

### Delete multiple models
```
  User.delete_all()  # delete all users
  User.delete_all(age=20) # delete all users which age = 20
```

## Retrieving Modles
```
  User.first()
  User.last()
  User.all()
  User.where(name='jon').first()
  User.where(age__lt=30).all()
```

### Aggregates
```
  User.count()
  User.max('age')
  User.min('age')
  User.avg('age')
  User.sum('age')
```
> just support: count、max、min、avg、sum


==
- articles
  - id
  - title
  - content
  - category_id

- categories
  - id
  - name

- tags
  - id
  - name

- article_tags
  - id
  - article_id
  - tag_id


Artcile.all()   ==> Collection (element type is Article)
> SELECT * FROM `articles`


Article.offset(10).first() ==> Article
> SELECT * FROM `articles` LIMIT 1 OFFSET 10


Article.first().category  ==> Category
> a = Article.first() ==> SELECT * FROM `articles` LIMIT 1
> a.categroy  ==> SELECT * FROM `categories` WHERE `categories`.`id` = 2 LIMIT 1


Article.with_('category').first().category ==> Category
> SELECT * FROM `articles` LIMIT 1
> SELECT * FROM `categories` WHERE `categories`.`id` IN (0)


Category.first().articles  ==> Collection (element type is Article)
> c = Category.first() ==> SELECT * FROM `categories` LIMIT 1
> c.articles  ==> SELECT * FROM `articles` WHERE `articles`.`category_id` = 1


Category.with_('articles').first().articles ==> Collection (elment type is Article)
> SELECT * FROM `categories` LIMIT 1
> SELECT * FROM `articles` WHERE `articles`.`category_id` IN (1)


Article.first().tags ==> Collection (element type is Tag)
> a = Article.first()
> 
>     SELECT * FROM `articles` LIMIT 1
>
> a.tags  ==> 
> 
>     SELECT 
>         *, 
>         `article_tags`.`article_id` AS `pivot_article_id`, 
>         `article_tags`.`tag_id` AS `pivot_tag_id` 
>     FROM 
>         `app_tag` 
>     INNER JOIN 
>         `article_tags` 
>     ON 
>         `app_tag`.`id` = `article_tags`.`tag_id` 
>     WHERE 
>         `article_tags`.`article_id` = 1


Article.with_('tags').first().tags ==> Collection (element type is Tag)
>     SELECT * FROM `articles` LIMIT 1
>
>     SELECT 
>       *, 
>       `article_tags`.`article_id` AS `pivot_article_id`, 
>       `article_tags`.`tag_id` AS `pivot_tag_id` 
>     FROM 
>       `app_tag` 
>     INNER JOIN 
>       `article_tags` 
>     ON 
>       `app_tag`.`id` = `article_tags`.`tag_id` 
>     WHERE 
>       `article_tags`.`article_id` IN (1)'
>
