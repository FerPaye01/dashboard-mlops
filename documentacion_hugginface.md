HfApi Client
Below is the documentation for the HfApi class, which serves as a Python wrapper for the Hugging Face Hub’s API.

All methods from the HfApi are also accessible from the package’s root directly. Both approaches are detailed below.

Using the root method is more straightforward but the HfApi class gives you more flexibility. In particular, you can pass a token that will be reused in all HTTP calls. This is different from hf auth login or login() as the token is not persisted on the machine. It is also possible to provide a different endpoint or configure a custom user-agent.

Copied
from huggingface_hub import HfApi, list_models

# Use root method
models = list_models()

# Or configure a HfApi client
hf_api = HfApi(
    endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
    token="hf_xxx", # Token is not persisted on the machine.
)
models = hf_api.list_models()
HfApi
class huggingface_hub.HfApi
<
source
>
( endpoint: str | None = Nonetoken: str | bool | None = Nonelibrary_name: str | None = Nonelibrary_version: str | None = Noneuser_agent: dict | str | None = Noneheaders: dict[str, str] | None = None )

Parameters

endpoint (str, optional) — Endpoint of the Hub. Defaults to https://huggingface.co.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
library_name (str, optional) — The name of the library that is making the HTTP request. Will be added to the user-agent header. Example: "transformers".
library_version (str, optional) — The version of the library that is making the HTTP request. Will be added to the user-agent header. Example: "4.24.0".
user_agent (str, dict, optional) — The user agent info in the form of a dictionary or a single string. It will be completed with information about the installed packages.
headers (dict, optional) — Additional headers to be sent with each request. Example: {"X-My-Header": "value"}. Headers passed here are taking precedence over the default headers.
Client to interact with the Hugging Face Hub via HTTP.

The client is initialized with some high-level settings used in all requests made to the Hub (HF endpoint, authentication, user agents…). Using the HfApi client is preferred but not mandatory as all of its public methods are exposed directly at the root of huggingface_hub.

accept_access_request
<
source
>
( repo_id: struser: strrepo_type: str | None = Nonetoken: bool | str | None = None )

Expand 4 parameters
Parameters

repo_id (str) — The id of the repo to accept access request for.
user (str) — The username of the user which access request should be accepted.
repo_type (str, optional) — The type of the repo to accept access request for. Must be one of model, dataset or space. Defaults to model.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

HfHubHTTPError

HfHubHTTPError — HTTP 400 if the repo is not gated.
HfHubHTTPError — HTTP 403 if you only have read-only access to the repo. This can be the case if you don’t have write or admin role in the organization the repo belongs to or if you passed a read token.
HfHubHTTPError — HTTP 404 if the user does not exist on the Hub.
HfHubHTTPError — HTTP 404 if the user access request cannot be found.
HfHubHTTPError — HTTP 404 if the user access request is already in the accepted list.

Accept an access request from a user for a given gated repo.

Once the request is accepted, the user will be able to download any file of the repo and access the community tab. If the approval mode is automatic, you don’t have to accept requests manually. An accepted request can be cancelled or rejected at any time using cancel_access_request() and reject_access_request().

For more info about gated repos, see https://huggingface.co/docs/hub/models-gated.

add_collection_item
<
source
>
( collection_slug: stritem_id: stritem_type: CollectionItemType_Tnote: str | None = Noneexists_ok: bool = Falsetoken: bool | str | None = None )

Parameters

collection_slug (str) — Slug of the collection to update. Example: "TheBloke/recent-models-64f9a55bb3115b4f513ec026".
item_id (str) — Id of the item to add to the collection. Use the repo_id for repos/spaces/datasets, the paper id for papers, the slug of another collection (e.g. "moonshotai/kimi-k2") or a bucket id (e.g. "namespace/bucket-name").
item_type (str) — Type of the item to add. Can be one of "model", "dataset", "space", "paper", "collection" or "bucket".
note (str, optional) — A note to attach to the item in the collection. The maximum size for a note is 500 characters.
exists_ok (bool, optional) — If True, do not raise an error if item already exists.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

HfHubHTTPError

HfHubHTTPError — HTTP 403 if you only have read-only access to the repo. This can be the case if you don’t have write or admin role in the organization the repo belongs to or if you passed a read token.
HfHubHTTPError — HTTP 404 if the item you try to add to the collection does not exist on the Hub.
HfHubHTTPError — HTTP 409 if the item you try to add to the collection is already in the collection (and exists_ok=False)

Add an item to a collection on the Hub.

Returns: Collection

Example:

Copied
from huggingface_hub import add_collection_item
collection = add_collection_item(
    collection_slug="davanstrien/climate-64f99dc2a5067f6b65531bab",
    item_id="pierre-loic/climate-news-articles",
    item_type="dataset"
)
collection.items[-1].item_id
"pierre-loic/climate-news-articles"
# ^item got added to the collection on last position

# Add item with a note
add_collection_item(
    collection_slug="davanstrien/climate-64f99dc2a5067f6b65531bab",
    item_id="datasets/climate_fever",
    item_type="dataset"
    note="This dataset adopts the FEVER methodology that consists of 1,535 real-world claims regarding climate-change collected on the internet."
)
(...)
add_space_secret
<
source
>
( repo_id: strkey: strvalue: strdescription: str | None = Nonetoken: bool | str | None = None )

Parameters

repo_id (str) — ID of the repo to update. Example: "bigcode/in-the-stack".
key (str) — Secret key. Example: "GITHUB_API_KEY"
value (str) — Secret value. Example: "your_github_api_key".
description (str, optional) — Secret description. Example: "Github API key to access the Github API".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Adds or updates a secret in a Space.

Secrets allow to set secret keys or tokens to a Space without hardcoding them. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets.

add_space_variable
<
source
>
( repo_id: strkey: strvalue: strdescription: str | None = Nonetoken: bool | str | None = None )

Parameters

repo_id (str) — ID of the repo to update. Example: "bigcode/in-the-stack".
key (str) — Variable key. Example: "MODEL_REPO_ID"
value (str) — Variable value. Example: "the_model_repo_id".
description (str) — Description of the variable. Example: "Model Repo ID of the implemented model".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Adds or updates a variable in a Space.

Variables allow to set environment variables to a Space without hardcoding them. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets-and-environment-variables

auth_check
<
source
>
( repo_id: strrepo_type: str | None = Nonetoken: bool | str | None = Nonewrite: bool = False )

Parameters

repo_id (str) — The repository to check for access. Format should be "user/repo_name". Example: "user/my-cool-model".
repo_type (str, optional) — The type of the repository. Should be one of "model", "dataset", or "space". If not specified, the default is "model".
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
write (bool, optional) — If True, checks whether the user has content write permission on the repository. If False (default), only checks for read access.
Raises

RepositoryNotFoundError or GatedRepoError

RepositoryNotFoundError — Raised if the repository does not exist, is private, or the user does not have access. This can occur if the repo_id or repo_type is incorrect or if the repository is private but the user is not authenticated.

GatedRepoError — Raised if the repository exists but is gated and the user is not authorized to access it.


Check if the provided user token has access to a specific repository on the Hugging Face Hub.

This method verifies whether the user, authenticated via the provided token, has access to the specified repository. If the repository is not found or if the user lacks the required permissions to access it, the method raises an appropriate exception.

Example:

Check if the user has access to a repository:

Copied
from huggingface_hub import auth_check
from huggingface_hub.utils import GatedRepoError, RepositoryNotFoundError

try:
    auth_check("user/my-cool-model")
except GatedRepoError:
    # Handle gated repository error
    print("You do not have permission to access this gated repository.")
except RepositoryNotFoundError:
    # Handle repository not found error
    print("The repository was not found or you do not have access.")
In this example:

If the user has access, the method completes successfully.
If the repository is gated or does not exist, appropriate exceptions are raised, allowing the user to handle them accordingly.
batch_bucket_files
<
source
>
( bucket_id: stradd: list[tuple[str | Path | bytes, str]] | None = Nonecopy: list[tuple[str, str, str, str]] | None = Nonedelete: list[str] | None = Nonetoken: str | bool | None = None )

Parameters

bucket_id (str) — The ID of the bucket (e.g. "username/my-bucket").
add (list of tuple, optional) — Files to upload. Each element is a (source, destination) tuple where source is a path to a local file (str or Path) or raw bytes content, and destination is the path in the bucket.
copy (list of tuple, optional) — Files to copy by xet hash. Each element is a (source_repo_type, source_repo_id, xet_hash, destination) tuple where:
source_repo_type is the type of the source repository: "model", "dataset", "space", or "bucket".
source_repo_id is the ID of the source repository or bucket (e.g. "username/my-model").
xet_hash is the xet hash of the file to copy.
destination is the destination path in the bucket. This is a server-side operation — no data is downloaded or re-uploaded.
delete (list of str, optional) — Paths of files to delete from the bucket.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Add, copy, and/or delete files in a bucket.

This is a non-transactional operation. If an error occurs in the process, some files may have been uploaded, copied, or deleted while others haven’t.

Example:

Copied
from huggingface_hub import batch_bucket_files

# Upload files
batch_bucket_files(
    "username/my-bucket",
    add=[
        ("./model.safetensors", "models/model.safetensors"),
        (b'{{"key": "value"}}', "config.json"),
    ],
)

# Copy xet files from another bucket or repo (server-side, no data transfer)
batch_bucket_files(
    "username/my-bucket",
    copy=[
        ("bucket", "username/source-bucket", "<xethash_1>", "models/model.safetensors"),
        ("model", "username/my-model", "<xethash_2>", "models/config.safetensors"),
    ],
)

# Delete files
batch_bucket_files("username/my-bucket", delete=["old-model.bin"])

# Upload and delete in one batch
batch_bucket_files(
    "username/my-bucket",
    add=[("./new.txt", "new.txt")],
    delete=["old.txt"],
)
bucket_info
<
source
>
( bucket_id: strtoken: bool | str | None = None ) → BucketInfo

Parameters

bucket_id (str) — The ID of the bucket (e.g. "username/my-bucket").
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

BucketInfo

The bucket information.


Raises

BucketNotFoundError or or

BucketNotFoundError — If the bucket cannot be found. This may be because it doesn’t exist,
or — because it is set to private and you do not have access.

Get information about a specific bucket on the Hub.

Example:

Copied
from huggingface_hub import bucket_info
info = bucket_info(bucket_id="Wauplin/first-bucket")
info.id
'Wauplin/first-bucket'
info.private
False
info.created_at
datetime.datetime(2026, 2, 6, 17, 37, 57, tzinfo=datetime.timezone.utc)
info.size
551879671
info.total_files
12
cancel_access_request
<
source
>
( repo_id: struser: strrepo_type: str | None = Nonetoken: bool | str | None = None )

Parameters

repo_id (str) — The id of the repo to cancel access request for.
user (str) — The username of the user which access request should be cancelled.
repo_type (str, optional) — The type of the repo to cancel access request for. Must be one of model, dataset or space. Defaults to model.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

HfHubHTTPError

HfHubHTTPError — HTTP 400 if the repo is not gated.
HfHubHTTPError — HTTP 403 if you only have read-only access to the repo. This can be the case if you don’t have write or admin role in the organization the repo belongs to or if you passed a read token.
HfHubHTTPError — HTTP 404 if the user does not exist on the Hub.
HfHubHTTPError — HTTP 404 if the user access request cannot be found.
HfHubHTTPError — HTTP 404 if the user access request is already in the pending list.

Cancel an access request from a user for a given gated repo.

A cancelled request will go back to the pending list and the user will lose access to the repo.

For more info about gated repos, see https://huggingface.co/docs/hub/models-gated.

cancel_job
<
source
>
( job_id: strnamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

job_id (str) — ID of the Job.
namespace (str, optional) — The namespace where the Job is running. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Cancel a compute Job on Hugging Face infrastructure.

change_discussion_status
<
source
>
( repo_id: strdiscussion_num: intnew_status: Literal['open', 'closed']token: bool | str | None = Nonecomment: str | None = Nonerepo_type: str | None = None ) → DiscussionStatusChange

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
discussion_num (int) — The number of the Discussion or Pull Request . Must be a strictly positive integer.
new_status (str) — The new status for the discussion, either "open" or "closed".
comment (str, optional) — An optional comment to post with the status change.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

DiscussionStatusChange

the status change event


Closes or re-opens a Discussion or Pull Request.

Examples:

Copied
new_title = "New title, fixing a typo"
HfApi().rename_discussion(
    repo_id="username/repo_name",
    discussion_num=34
    new_title=new_title
)
# DiscussionStatusChange(id='deadbeef0000000', type='status-change', ...)
Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
comment_discussion
<
source
>
( repo_id: strdiscussion_num: intcomment: strtoken: bool | str | None = Nonerepo_type: str | None = None ) → DiscussionComment

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
discussion_num (int) — The number of the Discussion or Pull Request . Must be a strictly positive integer.
comment (str) — The content of the comment to create. Comments support markdown formatting.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

DiscussionComment

the newly created comment


Creates a new comment on the given Discussion.

Examples:

Copied

comment = """
Hello @otheruser!
...
# This is a title
...
**This is bold**, *this is italic* and ~this is strikethrough~
And [this](http://url) is a link
"""

HfApi().comment_discussion(
    repo_id="username/repo_name",
    discussion_num=34
    comment=comment
)
# DiscussionComment(id='deadbeef0000000', type='comment', ...)
Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
copy_files
<
source
>
( source: strdestination: strtoken: str | bool | None = None )

Parameters

source (str) — Source location as an hf:// URI. Can be a bucket path (e.g. "hf://buckets/my-bucket/path/to/file") or a repo path (e.g. "hf://username/my-model/weights.bin", "hf://datasets/username/my-dataset/data/").
destination (str) — Destination location as an hf:// URI pointing to a bucket (e.g. "hf://buckets/my-bucket/target/path") or a repository (e.g. "hf://username/my-model/target/path").
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

ValueError

ValueError — If source/destination URIs are invalid or if copying from a bucket to a repo.

Copy files between locations on the Hub.

Copy files from a bucket or repository (model, dataset, space) to a bucket or another repository. Both individual files and entire folders are supported.

When copying folders, a trailing / on the source path uses rsync-style semantics: copy the contents of the folder into the destination, without nesting the source folder itself. Without a trailing /, the source folder is nested inside the destination (like cp -r).

When copying from a repository to a bucket, .gitattributes files are automatically excluded since they are git-specific metadata and not relevant in a bucket context.

Repo-to-repo copies use CommitOperationCopy under the hood and create a commit on the destination repository. Bucket-to-repo copies are not supported.

Server-side copies only work within the same storage region.

Example:

Copied
from huggingface_hub import copy_files

# Copy a single file between buckets
copy_files("hf://buckets/my-bucket/data.bin", "hf://buckets/other-bucket/data.bin")

# Copy a folder into another bucket (nests: backup/models/...)
copy_files("hf://buckets/my-bucket/models", "hf://buckets/other-bucket/backup/")

# Copy folder contents (trailing /): files go directly into backup/
copy_files("hf://buckets/my-bucket/models/", "hf://buckets/other-bucket/backup/")

# Copy a file from a model repo to a bucket
copy_files("hf://username/my-model/model.safetensors", "hf://buckets/my-bucket/")

# Copy an entire dataset to a bucket
copy_files("hf://datasets/username/my-dataset/", "hf://buckets/my-bucket/datasets/")

# Copy files between repositories
copy_files("hf://username/source-model/", "hf://username/dest-model/")

# Copy a file from one repo to another
copy_files("hf://username/source-model/config.json", "hf://username/dest-model/config.json")
create_branch
<
source
>
( repo_id: strbranch: strrevision: str | None = Nonetoken: bool | str | None = Nonerepo_type: str | None = Noneexist_ok: bool = False )

Parameters

repo_id (str) — The repository in which the branch will be created. Example: "user/my-cool-model".
branch (str) — The name of the branch to create.
revision (str, optional) — The git revision to create the branch from. It can be a branch name or the OID/SHA of a commit, as a hexadecimal string. Defaults to the head of the "main" branch.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if creating a branch on a dataset or space, None or "model" if tagging a model. Default is None.
exist_ok (bool, optional, defaults to False) — If True, do not raise an error if branch already exists.
Raises

RepositoryNotFoundError or BadRequestError or HfHubHTTPError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.
BadRequestError — If invalid reference for a branch. Ex: refs/pr/5 or ‘refs/foo/bar’.
HfHubHTTPError — If the branch already exists on the repo (error 409) and exist_ok is set to False.

Create a new branch for a repo on the Hub, starting from the specified revision (defaults to main). To find a revision suiting your needs, you can use list_repo_refs() or list_repo_commits().

create_bucket
<
source
>
( bucket_id: strprivate: bool | None = Noneresource_group_id: str | None = Noneregion: REPO_REGIONS | None = Noneexist_ok: bool = Falsetoken: bool | str | None = None ) → BucketUrl

Parameters

bucket_id (str) — A namespace (user or an organization) and a bucket name separated by a /. If no namespace is provided, the bucket will be created in the current user’s namespace.
private (bool, optional) — Whether to make the bucket private. If None (default), the bucket will be public unless the organization’s default is private.
resource_group_id (str, optional) — Resource group in which to create the bucket. Resource groups are only available for Enterprise Hub organizations and allow to define which members of the organization can access the resource. The ID of a resource group can be found in the URL of the resource’s page on the Hub (e.g. "66670e5163145ca562cb1988"). To learn more about resource groups, see https://huggingface.co/docs/hub/en/security-resource-groups.
region (Literal["us", "eu"], optional) — Cloud region in which to create the bucket. Can be one of "us" or "eu". If not specified, the bucket will be created in the default region. Requires Team plan or above.
exist_ok (bool, optional, defaults to False) — If True, do not raise an error if the bucket already exists.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

BucketUrl

URL to the newly created bucket containing attributes like endpoint, namespace, and bucket_id.


Create a bucket on the Hub.

Example:

Copied
from huggingface_hub import create_bucket

url = create_bucket(bucket_id="my-bucket")
url.bucket_id
'user/my-bucket'
url.url
'https://huggingface.co/buckets/user/my-bucket'
url.uri.to_uri()
'hf://buckets/user/my-bucket'

create_bucket(bucket_id="my-bucket", private=True, exist_ok=True)
BucketUrl(...)

create_bucket(bucket_id="my-bucket", region="us")
BucketUrl(...)
create_collection
<
source
>
( title: strnamespace: str | None = Nonedescription: str | None = Noneprivate: bool = Falseexists_ok: bool = Falsetoken: bool | str | None = None )

Parameters

title (str) — Title of the collection to create. Example: "Recent models".
namespace (str, optional) — Namespace of the collection to create (username or org). Will default to the owner name.
description (str, optional) — Description of the collection to create.
private (bool, optional) — Whether the collection should be private or not. Defaults to False (i.e. public collection).
exists_ok (bool, optional) — If True, do not raise an error if collection already exists.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Create a new Collection on the Hub.

Returns: Collection

Example:

Copied
from huggingface_hub import create_collection
collection = create_collection(
    title="ICCV 2023",
    description="Portfolio of models, papers and demos I presented at ICCV 2023",
)
collection.slug
"username/iccv-2023-64f9a55bb3115b4f513ec026"
create_commit
<
source
>
( repo_id: stroperations: Iterable[CommitOperation]commit_message: strcommit_description: str | None = Nonetoken: str | bool | None = Nonerepo_type: str | None = Nonerevision: str | None = Nonecreate_pr: bool | None = Nonenum_threads: int = 5parent_commit: str | None = Nonerun_as_future: bool = False_hot_reload: bool | None = None ) → CommitInfo or Future

Parameters

repo_id (str) — The repository in which the commit will be created, for example: "username/custom_transformers"
operations (Iterable of CommitOperation()) — An iterable of operations to include in the commit, either:
CommitOperationAdd to upload a file
CommitOperationDelete to delete a file
CommitOperationCopy to copy a file
Operation objects will be mutated to include information relative to the upload. Do not reuse the same objects for multiple commits.

commit_message (str) — The summary (first line) of the commit that will be created.
commit_description (str, optional) — The description of the commit that will be created
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
revision (str, optional) — The git revision to commit from. Defaults to the head of the "main" branch.
create_pr (boolean, optional) — Whether or not to create a Pull Request with that commit. Defaults to False. If revision is not set, PR is opened against the "main" branch. If revision is set and is a branch, PR is opened against this branch. If revision is set and is not a branch name (example: a commit oid), an RevisionNotFoundError is returned by the server.
num_threads (int, optional) — Number of concurrent threads for uploading files. Defaults to 5. Setting it to 2 means at most 2 files will be uploaded concurrently.
parent_commit (str, optional) — The OID / SHA of the parent commit, as a hexadecimal string. Shorthands (7 first characters) are also supported. If specified and create_pr is False, the commit will fail if revision does not point to parent_commit. If specified and create_pr is True, the pull request will be created from parent_commit. Specifying parent_commit ensures the repo has not changed before committing the changes, and can be especially useful if the repo is updated / committed to concurrently.
run_as_future (bool, optional) — Whether or not to run this method in the background. Background jobs are run sequentially without blocking the main thread. Passing run_as_future=True will return a Future object. Defaults to False.
Returns

CommitInfo or Future

Instance of CommitInfo containing information about the newly created commit (commit hash, commit url, pr url, commit message,…). If run_as_future=True is passed, returns a Future object which will contain the result when executed.


Raises

ValueError or RepositoryNotFoundError

ValueError — If commit message is empty.
ValueError — If parent commit is not a valid commit OID.
ValueError — If a README.md file with an invalid metadata section is committed. In this case, the commit will fail early, before trying to upload any file.
ValueError — If create_pr is True and revision is neither None nor "main".
RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.

Creates a commit in the given repo, deleting & uploading files as needed.

The input list of CommitOperation will be mutated during the commit process. Do not reuse the same objects for multiple commits.

create_commit assumes that the repo already exists on the Hub. If you get a Client error 404, please make sure you are authenticated, that your token has the required permissions, and that repo_id and repo_type are set correctly. If repo does not exist, create it first using create_repo().

create_commit is limited to 25k LFS files and a 1GB payload for regular files.

create_discussion
<
source
>
( repo_id: strtitle: strtoken: bool | str | None = Nonedescription: str | None = Nonerepo_type: str | None = Nonepull_request: bool = False )

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
title (str) — The title of the discussion. It can be up to 200 characters long, and must be at least 3 characters long. Leading and trailing whitespaces will be stripped.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
description (str, optional) — An optional description for the Pull Request. Defaults to "Discussion opened with the huggingface_hub Python library"
pull_request (bool, optional) — Whether to create a Pull Request or discussion. If True, creates a Pull Request. If False, creates a discussion. Defaults to False.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
Creates a Discussion or Pull Request.

Pull Requests created programmatically will be in "draft" status.

Creating a Pull Request with changes can also be done at once with HfApi.create_commit().

Returns: DiscussionWithDetails

Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
create_inference_endpoint
<
source
>
( name: strrepository: strframework: straccelerator: strinstance_size: strinstance_type: strregion: strvendor: straccount_id: str | None = Nonemin_replica: int = 1max_replica: int = 1scaling_metric: InferenceEndpointScalingMetric | None = Nonescaling_threshold: float | None = Nonescale_to_zero_timeout: int | None = Nonerevision: str | None = Nonetask: str | None = Nonecustom_image: dict | None = Nonecontainer_command: list[str] | None = Nonecontainer_args: list[str] | None = Noneenv: dict[str, str] | None = Nonesecrets: dict[str, str] | None = Nonetype: InferenceEndpointType | str = <InferenceEndpointType.AUTHENTICATED: 'authenticated'>domain: str | None = Nonepath: str | None = Nonecache_http_responses: bool | None = Nonetags: list[str] | None = Nonenamespace: str | None = Nonetoken: bool | str | None = None ) → InferenceEndpoint

Parameters

name (str) — The unique name for the new Inference Endpoint.
repository (str) — The name of the model repository associated with the Inference Endpoint (e.g. "gpt2").
framework (str) — The machine learning framework used for the model (e.g. "custom").
accelerator (str) — The hardware accelerator to be used for inference (e.g. "cpu").
instance_size (str) — The size or type of the instance to be used for hosting the model (e.g. "x4").
instance_type (str) — The cloud instance type where the Inference Endpoint will be deployed (e.g. "intel-icl").
region (str) — The cloud region in which the Inference Endpoint will be created (e.g. "us-east-1").
vendor (str) — The cloud provider or vendor where the Inference Endpoint will be hosted (e.g. "aws").
account_id (str, optional) — The account ID used to link a VPC to a private Inference Endpoint (if applicable).
min_replica (int, optional) — The minimum number of replicas (instances) to keep running for the Inference Endpoint. To enable scaling to zero, set this value to 0 and adjust scale_to_zero_timeout accordingly. Defaults to 1.
max_replica (int, optional) — The maximum number of replicas (instances) to scale to for the Inference Endpoint. Defaults to 1.
scaling_metric (str or InferenceEndpointScalingMetric , optional) — The metric reference for scaling. Either “pendingRequests” or “hardwareUsage” when provided. Defaults to None (meaning: let the HF Endpoints service specify the metric).
scaling_threshold (float, optional) — The scaling metric threshold used to trigger a scale up. Ignored when scaling metric is not provided. Defaults to None (meaning: let the HF Endpoints service specify the threshold).
scale_to_zero_timeout (int, optional) — The duration in minutes before an inactive endpoint is scaled to zero, or no scaling to zero if set to None and min_replica is not 0. Defaults to None.
revision (str, optional) — The specific model revision to deploy on the Inference Endpoint (e.g. "6c0e6080953db56375760c0471a8c5f2929baf11").
task (str, optional) — The task on which to deploy the model (e.g. "text-classification").
custom_image (dict, optional) — A custom Docker image to use for the Inference Endpoint. This is useful if you want to deploy an Inference Endpoint running on the text-generation-inference (TGI) framework or a custom container (see examples).
container_command (list[str], optional) — Override the container entrypoint command (maps to model.command in the API payload). Typically used together with custom_image.
container_args (list[str], optional) — Arguments appended to the container entrypoint (maps to model.args in the API payload). Typically used together with custom_image to pass runtime flags to the container.
env (dict[str, str], optional) — Non-secret environment variables to inject in the container environment.
secrets (dict[str, str], optional) — Secret values to inject in the container environment.
type ([`InferenceEndpointType], *optional*) -- The type of the Inference Endpoint, which can be “authenticated”(default),“public”or“private”. “protected”is deprecated in favor of“authenticated”` and will be removed in a future release.
domain (str, optional) — The custom domain for the Inference Endpoint deployment, if setup the inference endpoint will be available at this domain (e.g. "my-new-domain.cool-website.woof").
path (str, optional) — The custom path to the deployed model, should start with a / (e.g. "/models/google-bert/bert-base-uncased").
cache_http_responses (bool, optional) — Whether to cache HTTP responses from the Inference Endpoint. Defaults to False.
tags (list[str], optional) — A list of tags to associate with the Inference Endpoint.
namespace (str, optional) — The namespace where the Inference Endpoint will be created. Defaults to the current user’s namespace.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

InferenceEndpoint

information about the updated Inference Endpoint.


Create a new Inference Endpoint.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
endpoint = api.create_inference_endpoint(
    "my-endpoint-name",
    repository="gpt2",
    framework="pytorch",
    task="text-generation",
    accelerator="cpu",
    vendor="aws",
    region="us-east-1",
    type="authenticated",
    instance_size="x2",
    instance_type="intel-icl",
)
endpoint
InferenceEndpoint(name='my-endpoint-name', status="pending",...)

# Run inference on the endpoint
endpoint.client.text_generation(...)
"..."
Copied
# Start an Inference Endpoint running Zephyr-7b-beta on TGI
from huggingface_hub import HfApi
api = HfApi()
endpoint = api.create_inference_endpoint(
    "aws-zephyr-7b-beta-0486",
    repository="HuggingFaceH4/zephyr-7b-beta",
    framework="pytorch",
    task="text-generation",
    accelerator="gpu",
    vendor="aws",
    region="us-east-1",
    type="authenticated",
    instance_size="x1",
    instance_type="nvidia-a10g",
    env={
          "MAX_BATCH_PREFILL_TOKENS": "2048",
          "MAX_INPUT_LENGTH": "1024",
          "MAX_TOTAL_TOKENS": "1512",
          "MODEL_ID": "/repository"
        },
    custom_image={
        "healthRoute": "/health",
        "url": "ghcr.io/huggingface/text-generation-inference:1.1.0",
    },
   secrets={"MY_SECRET_KEY": "secret_value"},
   tags=["dev", "text-generation"],
)
Copied
# Start an Inference Endpoint running ProsusAI/finbert while scaling to zero in 15 minutes
from huggingface_hub import HfApi
api = HfApi()
endpoint = api.create_inference_endpoint(
    "finbert-classifier",
    repository="ProsusAI/finbert",
    framework="pytorch",
    task="text-classification",
    min_replica=0,
    scale_to_zero_timeout=15,
    accelerator="cpu",
    vendor="aws",
    region="us-east-1",
    type="authenticated",
    instance_size="x2",
    instance_type="intel-icl",
)
endpoint.wait(timeout=300)
# Run inference on the endpoint
endpoint.client.text_generation(...)
TextClassificationOutputElement(label='positive', score=0.8983615040779114)
create_inference_endpoint_from_catalog
<
source
>
( repo_id: strname: str | None = Noneaccelerator: Literal['cpu', 'gpu', 'neuron'] | str | None = Nonetoken: bool | str | None = Nonenamespace: str | None = None ) → InferenceEndpoint

Parameters

repo_id (str) — The ID of the model in the catalog to deploy as an Inference Endpoint.
name (str, optional) — The unique name for the new Inference Endpoint. If not provided, a random name will be generated.
accelerator (str, optional) — The hardware accelerator to be used for inference. Possible values include "cpu", "gpu", and "neuron". If not provided, the server will use a default appropriate for the model.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication).
namespace (str, optional) — The namespace where the Inference Endpoint will be created. Defaults to the current user’s namespace.
Returns

InferenceEndpoint

information about the new Inference Endpoint.


Create a new Inference Endpoint from a model in the Hugging Face Inference Catalog.

The goal of the Inference Catalog is to provide a curated list of models that are optimized for inference and for which default configurations have been tested. See https://endpoints.huggingface.co/catalog for a list of available models in the catalog.

create_inference_endpoint_from_catalog is experimental. Its API is subject to change in the future. Please provide feedback if you have any suggestions or requests.

create_pull_request
<
source
>
( repo_id: strtitle: strtoken: bool | str | None = Nonedescription: str | None = Nonerepo_type: str | None = None )

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
title (str) — The title of the discussion. It can be up to 200 characters long, and must be at least 3 characters long. Leading and trailing whitespaces will be stripped.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
description (str, optional) — An optional description for the Pull Request. Defaults to "Discussion opened with the huggingface_hub Python library"
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
Creates a Pull Request . Pull Requests created programmatically will be in "draft" status.

Creating a Pull Request with changes can also be done at once with HfApi.create_commit();

This is a wrapper around HfApi.create_discussion().

Returns: DiscussionWithDetails

Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
create_repo
<
source
>
( repo_id: strtoken: str | bool | None = Noneprivate: bool | None = Nonevisibility: RepoVisibility_T | None = Nonerepo_type: str | None = Noneexist_ok: bool = Falseresource_group_id: str | None = Noneregion: REPO_REGIONS | None = Nonespace_sdk: str | None = Nonespace_hardware: SpaceHardware | None = Nonespace_storage: SpaceStorage | None = Nonespace_sleep_time: int | None = Nonespace_secrets: list[dict[str, str]] | None = Nonespace_variables: list[dict[str, str]] | None = Nonespace_volumes: list[Volume] | None = None ) → RepoUrl

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
private (bool, optional) — Whether to make the repo private. If None (default), the repo will be public unless the organization’s default is private. This value is ignored if the repo already exists. Cannot be passed together with visibility.
visibility (Literal["public", "private", "protected"], optional) — Visibility of the repo. Can be "public" or "private", or "protected" for Spaces. If None (default), the repo will be public unless the organization’s default is private. This value is ignored if the repo already exists.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
exist_ok (bool, optional, defaults to False) — If True, do not raise an error if repo already exists.
resource_group_id (str, optional) — Resource group in which to create the repo. Resource groups is only available for Enterprise Hub organizations and allow to define which members of the organization can access the resource. The ID of a resource group can be found in the URL of the resource’s page on the Hub (e.g. "66670e5163145ca562cb1988"). To learn more about resource groups, see https://huggingface.co/docs/hub/en/security-resource-groups.
region (Literal["us", "eu"], optional) — Cloud region in which to create the repo. Can be one of "us" or "eu". If not specified, the repo will be created in the default region. Requires Team plan or above.
space_sdk (str, optional) — Choice of SDK to use if repo_type is “space”. Can be “streamlit”, “gradio”, “docker”, or “static”.
space_hardware (SpaceHardware or str, optional) — Choice of Hardware if repo_type is “space”. See SpaceHardware for a complete list.
space_storage (SpaceStorage or str, optional) — set_space_volumes instead> Choice of persistent storage tier. Example: "small". See SpaceStorage for a complete list.
space_sleep_time (int, optional) — Number of seconds of inactivity to wait before a Space is put to sleep. Set to -1 if you don’t want your Space to sleep (default behavior for upgraded hardware). For free hardware, you can’t configure the sleep time (value is fixed to 48 hours of inactivity). See https://huggingface.co/docs/hub/spaces-gpus#sleep-time for more details.
space_secrets (list[dict[str, str]], optional) — A list of secret keys to set in your Space. Each item is in the form {"key": ..., "value": ..., "description": ...} where description is optional. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets.
space_variables (list[dict[str, str]], optional) — A list of public environment variables to set in your Space. Each item is in the form {"key": ..., "value": ..., "description": ...} where description is optional. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets-and-environment-variables.
space_volumes (list[Volume], optional) — A list of Volume objects to mount in the Space at creation time. Each volume has a type ("bucket", "model", "dataset", or "space"), a source (repo or bucket ID), a mount_path (path inside the container), and optional revision, read_only, and path fields. Only applicable if repo_type is “space”.
Returns

RepoUrl

URL to the newly created repo. Value is a subclass of str containing attributes like endpoint, repo_type and repo_id.


Create an empty repo on the HuggingFace Hub.

create_scheduled_job
<
source
>
( image: strcommand: list[str]schedule: strsuspend: bool | None = Noneconcurrency: bool | None = Noneenv: dict[str, Any] | None = Nonesecrets: dict[str, Any] | None = Noneflavor: JobHardware | str | None = Nonetimeout: int | float | str | None = Nonelabels: dict[str, str] | None = Nonevolumes: list[Volume] | None = Noneexpose: list[int] | None = Nonenamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

image (str) — The Docker image to use. Examples: "ubuntu", "python:3.12", "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel". Example with an image from a Space: "hf.co/spaces/lhoestq/duckdb".
command (list[str]) — The command to run. Example: ["echo", "hello"].
schedule (str) — One of “@annually”, “@yearly”, “@monthly”, “@weekly”, “@daily”, “@hourly”, or a CRON schedule expression (e.g., ‘0 9 * * 1’ for 9 AM every Monday).
suspend (bool, optional) — If True, the scheduled Job is suspended (paused). Defaults to False.
concurrency (bool, optional) — If True, multiple instances of this Job can run concurrently. Defaults to False.
env (dict[str, Any], optional) — Defines the environment variables for the Job.
secrets (dict[str, Any], optional) — Defines the secret environment variables for the Job.
flavor (str, optional) — Flavor for the hardware. See JobHardware for possible values. Defaults to "cpu-basic".
timeout (Union[int, float, str], optional) — Max duration for the Job: int/float with s (seconds, default), m (minutes), h (hours) or d (days). Example: 300 or "5m" for 5 minutes.
labels (dict[str, str], optional) — Labels to attach to the job (key-value pairs).
volumes (list[Volume], optional) — Hugging Face Buckets or Repos to mount as volumes in the job container. Each volume is a Volume with type ("bucket", "model", "dataset", or "space"), source (e.g. "username/my-bucket"), and mount_path (e.g. "/data").
expose (list[int], optional) — Container ports to expose through the jobs proxy. Each listed port is reachable on the public jobs domain (e.g. https://<job_id>--8000.hf.jobs). Access always requires an HF token with read access to the job’s namespace.
namespace (str, optional) — The namespace where the Job will be created. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Create scheduled compute Jobs on Hugging Face infrastructure.

Example:

Create your first scheduled Job:

Copied
from huggingface_hub import create_scheduled_job
create_scheduled_job(image="python:3.12", command=["python", "-c" ,"print('Hello from HF compute!')"], schedule="@hourly")
Use a CRON schedule expression:

Copied
from huggingface_hub import create_scheduled_job
create_scheduled_job(image="python:3.12", command=["python", "-c" ,"print('this runs every 5min')"], schedule="*/5 * * * *")
Create a scheduled GPU Job:

Copied
from huggingface_hub import create_scheduled_job
image = "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel"
command = ["python", "-c", "import torch; print(f"This code ran with the following GPU: {torch.cuda.get_device_name()}")"]
create_scheduled_job(image, command, flavor="a10g-small", schedule="@hourly")
create_scheduled_uv_job
<
source
>
( script: strscript_args: list[str] | None = Noneschedule: strsuspend: bool | None = Noneconcurrency: bool | None = Nonedependencies: list[str] | None = Nonepython: str | None = Noneimage: str | None = Noneenv: dict[str, Any] | None = Nonesecrets: dict[str, Any] | None = Noneflavor: JobHardware | str | None = Nonetimeout: int | float | str | None = Nonelabels: dict[str, str] | None = Nonevolumes: list[Volume] | None = Noneexpose: list[int] | None = Nonenamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

script (str) — Path or URL of the UV script, or a command.
script_args (list[str], optional) — Arguments to pass to the script, or a command.
schedule (str) — One of “@annually”, “@yearly”, “@monthly”, “@weekly”, “@daily”, “@hourly”, or a CRON schedule expression (e.g., ‘0 9 * * 1’ for 9 AM every Monday).
suspend (bool, optional) — If True, the scheduled Job is suspended (paused). Defaults to False.
concurrency (bool, optional) — If True, multiple instances of this Job can run concurrently. Defaults to False.
dependencies (list[str], optional) — Dependencies to use to run the UV script.
python (str, optional) — Use a specific Python version. Default is 3.12.
image (str, optional, defaults to “ghcr.io/astral-sh/uv —python3.12-bookworm”): Use a custom Docker image with uv installed.
env (dict[str, Any], optional) — Defines the environment variables for the Job.
secrets (dict[str, Any], optional) — Defines the secret environment variables for the Job.
flavor (str, optional) — Flavor for the hardware. See JobHardware for possible values. Defaults to "cpu-basic".
timeout (Union[int, float, str], optional) — Max duration for the Job: int/float with s (seconds, default), m (minutes), h (hours) or d (days). Example: 300 or "5m" for 5 minutes.
labels (dict[str, str], optional) — Labels to attach to the job (key-value pairs).
volumes (list[Volume], optional) — Hugging Face Buckets or Repos to mount as volumes in the job container. Each volume is a Volume with type ("bucket", "model", "dataset", or "space"), source (e.g. "username/my-bucket"), and mount_path (e.g. "/data").
expose (list[int], optional) — Container ports to expose through the jobs proxy. Each listed port is reachable on the public jobs domain (e.g. https://<job_id>--8000.hf.jobs). Access always requires an HF token with read access to the job’s namespace.
namespace (str, optional) — The namespace where the Job will be created. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Run a UV script Job on Hugging Face infrastructure.

Example:

Schedule a script from a URL:

Copied
from huggingface_hub import create_scheduled_uv_job
script = "https://raw.githubusercontent.com/huggingface/trl/refs/heads/main/trl/scripts/sft.py"
script_args = ["--model_name_or_path", "Qwen/Qwen2-0.5B", "--dataset_name", "trl-lib/Capybara", "--push_to_hub"]
create_scheduled_uv_job(script, script_args=script_args, dependencies=["trl"], flavor="a10g-small", schedule="@weekly")
Schedule a local script:

Copied
from huggingface_hub import create_scheduled_uv_job
script = "my_sft.py"
script_args = ["--model_name_or_path", "Qwen/Qwen2-0.5B", "--dataset_name", "trl-lib/Capybara", "--push_to_hub"]
create_scheduled_uv_job(script, script_args=script_args, dependencies=["trl"], flavor="a10g-small", schedule="@weekly")
Schedule a command:

Copied
from huggingface_hub import create_scheduled_uv_job
script = "lighteval"
script_args= ["endpoint", "inference-providers", "model_name=openai/gpt-oss-20b,provider=auto", "lighteval|gsm8k|0|0"]
create_scheduled_uv_job(script, script_args=script_args, dependencies=["lighteval"], flavor="a10g-small", schedule="@weekly")
create_tag
<
source
>
( repo_id: strtag: strtag_message: str | None = Nonerevision: str | None = Nonetoken: bool | str | None = Nonerepo_type: str | None = Noneexist_ok: bool = False )

Parameters

repo_id (str) — The repository in which a commit will be tagged. Example: "user/my-cool-model".
tag (str) — The name of the tag to create.
tag_message (str, optional) — The description of the tag to create.
revision (str, optional) — The git revision to tag. It can be a branch name or the OID/SHA of a commit, as a hexadecimal string. Shorthands (7 first characters) are also supported. Defaults to the head of the "main" branch.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if tagging a dataset or space, None or "model" if tagging a model. Default is None.
exist_ok (bool, optional, defaults to False) — If True, do not raise an error if tag already exists.
Raises

RepositoryNotFoundError or RevisionNotFoundError or HfHubHTTPError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.
RevisionNotFoundError — If revision is not found (error 404) on the repo.
HfHubHTTPError — If the branch already exists on the repo (error 409) and exist_ok is set to False.

Tag a given commit of a repo on the Hub.

create_webhook
<
source
>
( url: str | None = Nonejob_id: str | None = Nonewatched: list[dict | WebhookWatchedItem]domains: list[constants.WEBHOOK_DOMAIN_T] | None = Nonesecret: str | None = Nonetoken: bool | str | None = None ) → WebhookInfo

Parameters

url (str) — URL to send the payload to.
job_id (str) — ID of the source Job to trigger with the webhook payload in the environment variable WEBHOOK_PAYLOAD. Additional environment variables are available for convenience: WEBHOOK_REPO_ID, WEBHOOK_REPO_TYPE and WEBHOOK_SECRET.
watched (list[WebhookWatchedItem]) — List of WebhookWatchedItem to be watched by the webhook. It can be users, orgs, models, datasets or spaces. Watched items can also be provided as plain dictionaries.
domains (list[Literal["repo", "discussion"]], optional) — List of domains to watch. It can be “repo”, “discussion” or both.
secret (str, optional) — A secret to sign the payload with.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

WebhookInfo

Info about the newly created webhook.


Create a new webhook.

The webhook can either send a payload to a URL, or trigger a Job to run on Hugging Face infrastructure. This function should be called with one of url or job_id, but not both.

Example:

Create a webhook that sends a payload to a URL

Copied
from huggingface_hub import create_webhook
payload = create_webhook(
    watched=[{"type": "user", "name": "julien-c"}, {"type": "org", "name": "HuggingFaceH4"}],
    url="https://webhook.site/a2176e82-5720-43ee-9e06-f91cb4c91548",
    domains=["repo", "discussion"],
    secret="my-secret",
)
print(payload)
WebhookInfo(
    id="654bbbc16f2ec14d77f109cc",
    url="https://webhook.site/a2176e82-5720-43ee-9e06-f91cb4c91548",
    job=None,
    watched=[WebhookWatchedItem(type="user", name="julien-c"), WebhookWatchedItem(type="org", name="HuggingFaceH4")],
    domains=["repo", "discussion"],
    secret="my-secret",
    disabled=False,
)
Run a Job and then create a webhook that triggers this Job

Copied
from huggingface_hub import create_webhook, run_job
job = run_job(
    image="ubuntu",
    command=["bash", "-c", r"echo An event occurred in $WEBHOOK_REPO_ID: $WEBHOOK_PAYLOAD"],
)
payload = create_webhook(
    watched=[{"type": "user", "name": "julien-c"}, {"type": "org", "name": "HuggingFaceH4"}],
    job_id=job.id,
    domains=["repo", "discussion"],
    secret="my-secret",
)
print(payload)
WebhookInfo(
    id="654bbbc16f2ec14d77f109cc",
    url=None,
    job=JobSpec(
        docker_image='ubuntu',
        space_id=None,
        command=['bash', '-c', 'echo An event occurred in $WEBHOOK_REPO_ID: $WEBHOOK_PAYLOAD'],
        arguments=[],
        environment={},
        secrets=[],
        flavor='cpu-basic',
        timeout=None,
        tags=None,
        arch=None
    ),
    watched=[WebhookWatchedItem(type="user", name="julien-c"), WebhookWatchedItem(type="org", name="HuggingFaceH4")],
    domains=["repo", "discussion"],
    secret="my-secret",
    disabled=False,
)
dataset_info
<
source
>
( repo_id: strrevision: str | None = Nonetimeout: float | None = Nonefiles_metadata: bool = Falseexpand: list[ExpandDatasetProperty_T] | None = Nonetoken: bool | str | None = None ) → hf_api.DatasetInfo

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
revision (str, optional) — The revision of the dataset repository from which to get the information.
timeout (float, optional) — Whether to set a timeout for the request to the Hub.
files_metadata (bool, optional) — Whether or not to retrieve metadata for files in the repository (size, LFS metadata, etc). Defaults to False.
expand (list[ExpandDatasetProperty_T], optional) — List properties to return in the response. When used, only the properties in the list will be returned. This parameter cannot be used if files_metadata is passed. Possible values are "author", "cardData", "citation", "createdAt", "disabled", "description", "downloads", "downloadsAllTime", "gated", "lastModified", "likes", "mainSize", "paperswithcode_id", "private", "siblings", "sha", "tags", "trendingScore", "usedStorage", and "resourceGroup".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

hf_api.DatasetInfo

The dataset repository information.


Get info on one specific dataset on huggingface.co.

Dataset can be private if you pass an acceptable token.

Raises the following errors:

RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
RevisionNotFoundError If the revision to download from cannot be found.
delete_branch
<
source
>
( repo_id: strbranch: strtoken: bool | str | None = Nonerepo_type: str | None = None )

Parameters

repo_id (str) — The repository in which a branch will be deleted. Example: "user/my-cool-model".
branch (str) — The name of the branch to delete.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if creating a branch on a dataset or space, None or "model" if tagging a model. Default is None.
Raises

RepositoryNotFoundError or HfHubHTTPError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.
HfHubHTTPError — If trying to delete a protected branch. Ex: main cannot be deleted.
HfHubHTTPError — If trying to delete a branch that does not exist.

Delete a branch from a repo on the Hub.

delete_bucket
<
source
>
( bucket_id: strmissing_ok: bool = Falsetoken: bool | str | None = None )

Parameters

bucket_id (str) — The ID of the bucket (e.g. "username/my-bucket").
missing_ok (bool, optional, defaults to False) — If True, do not raise an error if the bucket does not exist.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

BucketNotFoundError

BucketNotFoundError — If the bucket cannot be found and missing_ok is set to False (default).

Delete a bucket from the Hub.

Example:

Copied
from huggingface_hub import delete_bucket
delete_bucket(bucket_id="Wauplin/first-bucket")
delete_bucket(bucket_id="Wauplin/first-bucket", missing_ok=True)
delete_collection
<
source
>
( collection_slug: strmissing_ok: bool = Falsetoken: bool | str | None = None )

Parameters

collection_slug (str) — Slug of the collection to delete. Example: "TheBloke/recent-models-64f9a55bb3115b4f513ec026".
missing_ok (bool, optional) — If True, do not raise an error if the collection doesn’t exist.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Delete a collection on the Hub.

Example:

Copied
from huggingface_hub import delete_collection
collection = delete_collection("username/useless-collection-64f9a55bb3115b4f513ec026", missing_ok=True)
This is a non-revertible action. A deleted collection cannot be restored.

delete_collection_item
<
source
>
( collection_slug: stritem_object_id: strmissing_ok: bool = Falsetoken: bool | str | None = None )

Parameters

collection_slug (str) — Slug of the collection to update. Example: "TheBloke/recent-models-64f9a55bb3115b4f513ec026".
item_object_id (str) — ID of the item in the collection. This is not the id of the item on the Hub (repo_id or paper id). It must be retrieved from a CollectionItem object. Example: collection.items[0].item_object_id.
missing_ok (bool, optional) — If True, do not raise an error if the item doesn’t exist.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Delete an item from a collection.

Example:

Copied
from huggingface_hub import get_collection, delete_collection_item

# Get collection first
collection = get_collection("TheBloke/recent-models-64f9a55bb3115b4f513ec026")

# Delete item based on its ID
delete_collection_item(
    collection_slug="TheBloke/recent-models-64f9a55bb3115b4f513ec026",
    item_object_id=collection.items[-1].item_object_id,
)
delete_file
<
source
>
( path_in_repo: strrepo_id: strtoken: str | bool | None = Nonerepo_type: str | None = Nonerevision: str | None = Nonecommit_message: str | None = Nonecommit_description: str | None = Nonecreate_pr: bool | None = Noneparent_commit: str | None = None )

Expand 9 parameters
Parameters

path_in_repo (str) — Relative filepath in the repo, for example: "checkpoints/1fec34a/weights.bin"
repo_id (str) — The repository from which the file will be deleted, for example: "username/custom_transformers"
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if the file is in a dataset or space, None or "model" if in a model. Default is None.
revision (str, optional) — The git revision to commit from. Defaults to the head of the "main" branch.
commit_message (str, optional) — The summary / title / first line of the generated commit. Defaults to f"Delete {path_in_repo} with huggingface_hub".
commit_description (str optional) — The description of the generated commit
create_pr (boolean, optional) — Whether or not to create a Pull Request with that commit. Defaults to False. If revision is not set, PR is opened against the "main" branch. If revision is set and is a branch, PR is opened against this branch. If revision is set and is not a branch name (example: a commit oid), an RevisionNotFoundError is returned by the server.
parent_commit (str, optional) — The OID / SHA of the parent commit, as a hexadecimal string. Shorthands (7 first characters) are also supported. If specified and create_pr is False, the commit will fail if revision does not point to parent_commit. If specified and create_pr is True, the pull request will be created from parent_commit. Specifying parent_commit ensures the repo has not changed before committing the changes, and can be especially useful if the repo is updated / committed to concurrently.
Deletes a file in the given repo.

Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
RevisionNotFoundError If the revision to download from cannot be found.
EntryNotFoundError If the file to download cannot be found.
delete_files
<
source
>
( repo_id: strdelete_patterns: list[str]token: bool | str | None = Nonerepo_type: str | None = Nonerevision: str | None = Nonecommit_message: str | None = Nonecommit_description: str | None = Nonecreate_pr: bool | None = Noneparent_commit: str | None = None )

Expand 9 parameters
Parameters

repo_id (str) — The repository from which the folder will be deleted, for example: "username/custom_transformers"
delete_patterns (list[str]) — List of files or folders to delete. Each string can either be a file path, a folder path, or a wildcard pattern. Patterns are Standard Wildcards (globbing patterns) as documented here. The pattern matching is based on fnmatch. Note that fnmatch matches * across path boundaries, unlike traditional Unix shell globbing. E.g. ["file.txt", "folder/", "data/*.parquet"]
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False. to the stored token.
repo_type (str, optional) — Type of the repo to delete files from. Can be "model", "dataset" or "space". Defaults to "model".
revision (str, optional) — The git revision to commit from. Defaults to the head of the "main" branch.
commit_message (str, optional) — The summary (first line) of the generated commit. Defaults to f"Delete files using huggingface_hub".
commit_description (str optional) — The description of the generated commit.
create_pr (boolean, optional) — Whether or not to create a Pull Request with that commit. Defaults to False. If revision is not set, PR is opened against the "main" branch. If revision is set and is a branch, PR is opened against this branch. If revision is set and is not a branch name (example: a commit oid), an RevisionNotFoundError is returned by the server.
parent_commit (str, optional) — The OID / SHA of the parent commit, as a hexadecimal string. Shorthands (7 first characters) are also supported. If specified and create_pr is False, the commit will fail if revision does not point to parent_commit. If specified and create_pr is True, the pull request will be created from parent_commit. Specifying parent_commit ensures the repo has not changed before committing the changes, and can be especially useful if the repo is updated / committed to concurrently.
Delete files from a repository on the Hub.

If a folder path is provided, the entire folder is deleted as well as all files it contained.

delete_folder
<
source
>
( path_in_repo: strrepo_id: strtoken: bool | str | None = Nonerepo_type: str | None = Nonerevision: str | None = Nonecommit_message: str | None = Nonecommit_description: str | None = Nonecreate_pr: bool | None = Noneparent_commit: str | None = None )

Expand 9 parameters
Parameters

path_in_repo (str) — Relative folder path in the repo, for example: "checkpoints/1fec34a".
repo_id (str) — The repository from which the folder will be deleted, for example: "username/custom_transformers"
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False. to the stored token.
repo_type (str, optional) — Set to "dataset" or "space" if the folder is in a dataset or space, None or "model" if in a model. Default is None.
revision (str, optional) — The git revision to commit from. Defaults to the head of the "main" branch.
commit_message (str, optional) — The summary / title / first line of the generated commit. Defaults to f"Delete folder {path_in_repo} with huggingface_hub".
commit_description (str optional) — The description of the generated commit.
create_pr (boolean, optional) — Whether or not to create a Pull Request with that commit. Defaults to False. If revision is not set, PR is opened against the "main" branch. If revision is set and is a branch, PR is opened against this branch. If revision is set and is not a branch name (example: a commit oid), an RevisionNotFoundError is returned by the server.
parent_commit (str, optional) — The OID / SHA of the parent commit, as a hexadecimal string. Shorthands (7 first characters) are also supported. If specified and create_pr is False, the commit will fail if revision does not point to parent_commit. If specified and create_pr is True, the pull request will be created from parent_commit. Specifying parent_commit ensures the repo has not changed before committing the changes, and can be especially useful if the repo is updated / committed to concurrently.
Deletes a folder in the given repo.

Simple wrapper around create_commit() method.

delete_inference_endpoint
<
source
>
( name: strnamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

name (str) — The name of the Inference Endpoint to delete.
namespace (str, optional) — The namespace in which the Inference Endpoint is located. Defaults to the current user.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Delete an Inference Endpoint.

This operation is not reversible. If you don’t want to be charged for an Inference Endpoint, it is preferable to pause it with pause_inference_endpoint() or scale it to zero with scale_to_zero_inference_endpoint().

For convenience, you can also delete an Inference Endpoint using InferenceEndpoint.delete().

delete_repo
<
source
>
( repo_id: strtoken: str | bool | None = Nonerepo_type: str | None = Nonemissing_ok: bool = False )

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model.
missing_ok (bool, optional, defaults to False) — If True, do not raise an error if repo does not exist.
Raises

RepositoryNotFoundError

RepositoryNotFoundError — If the repository to delete from cannot be found and missing_ok is set to False (default).

Delete a repo from the HuggingFace Hub. CAUTION: this is irreversible.

delete_scheduled_job
<
source
>
( scheduled_job_id: strnamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

scheduled_job_id (str) — ID of the scheduled Job.
namespace (str, optional) — The namespace where the scheduled Job is. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Delete a scheduled compute Job on Hugging Face infrastructure.

delete_space_secret
<
source
>
( repo_id: strkey: strtoken: bool | str | None = None )

Parameters

repo_id (str) — ID of the repo to update. Example: "bigcode/in-the-stack".
key (str) — Secret key. Example: "GITHUB_API_KEY".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Deletes a secret from a Space.

Secrets allow to set secret keys or tokens to a Space without hardcoding them. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets.

delete_space_storage
<
source
>
( repo_id: strtoken: bool | str | None = None ) → SpaceRuntime

Parameters

repo_id (str) — ID of the Space to update. Example: "open-llm-leaderboard/open_llm_leaderboard".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SpaceRuntime

Runtime information about a Space including Space stage and hardware.


Raises

BadRequestError

BadRequestError — If space has no persistent storage.

Delete persistent storage for a Space.

delete_space_storage is deprecated and will be removed in version 2.0. Use delete_space_volumes() instead.

delete_space_variable
<
source
>
( repo_id: strkey: strtoken: bool | str | None = None )

Parameters

repo_id (str) — ID of the repo to update. Example: "bigcode/in-the-stack".
key (str) — Variable key. Example: "MODEL_REPO_ID"
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Deletes a variable from a Space.

Variables allow to set environment variables to a Space without hardcoding them. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets-and-environment-variables

delete_space_volumes
<
source
>
( repo_id: strtoken: bool | str | None = None )

Parameters

repo_id (str) — ID of the Space to update. Example: "username/my-space".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

BadRequestError

BadRequestError — If the Space has no volumes attached.

Remove all volumes from a Space.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
api.delete_space_volumes("username/my-space")
delete_tag
<
source
>
( repo_id: strtag: strtoken: bool | str | None = Nonerepo_type: str | None = None )

Parameters

repo_id (str) — The repository in which a tag will be deleted. Example: "user/my-cool-model".
tag (str) — The name of the tag to delete.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if tagging a dataset or space, None or "model" if tagging a model. Default is None.
Raises

RepositoryNotFoundError or RevisionNotFoundError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.
RevisionNotFoundError — If tag is not found.

Delete a tag from a repo on the Hub.

delete_webhook
<
source
>
( webhook_id: strtoken: bool | str | None = None ) → None

Parameters

webhook_id (str) — The unique identifier of the webhook to delete.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

None

Delete a webhook.

Example:

Copied
from huggingface_hub import delete_webhook
delete_webhook("654bbbc16f2ec14d77f109cc")
disable_space_dev_mode
<
source
>
( repo_id: strtoken: bool | str | None = None ) → SpaceRuntime

Expand 2 parameters
Parameters

repo_id (str) — ID of the Space to disable dev mode. Example: "Salesforce/BLIP2".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SpaceRuntime

Runtime information about your Space.


Raises

RepositoryNotFoundError or HfHubHTTPError or BadRequestError

RepositoryNotFoundError — If your Space is not found (error 404). Most probably wrong repo_id or your space is private but you are not authenticated.
HfHubHTTPError — 403 Forbidden: only the owner of a Space can set dev mode. If you want to handle a Space that you don’t own, either ask the owner by opening a Discussion or duplicate the Space.
BadRequestError — If your Space is a static Space. Static Spaces are always running and never billed. If you want to hide a static Space, you can set it to private.

Disable dev mode on a Space.

Spaces Dev Mode eases the debugging of your application and makes iterating on Spaces faster by allowing you to restart your application without stopping the Space container itself. This feature is available as part of a PRO or Team & Enterprise plan. See https://huggingface.co/docs/hub/spaces-dev-mode for more details.

disable_webhook
<
source
>
( webhook_id: strtoken: bool | str | None = None ) → WebhookInfo

Parameters

webhook_id (str) — The unique identifier of the webhook to disable.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

WebhookInfo

Info about the disabled webhook.


Disable a webhook (makes it “disabled”).

Example:

Copied
from huggingface_hub import disable_webhook
disabled_webhook = disable_webhook("654bbbc16f2ec14d77f109cc")
disabled_webhook
WebhookInfo(
    id="654bbbc16f2ec14d77f109cc",
    url="https://webhook.site/a2176e82-5720-43ee-9e06-f91cb4c91548",
    jon=None,
    watched=[WebhookWatchedItem(type="user", name="julien-c"), WebhookWatchedItem(type="org", name="HuggingFaceH4")],
    domains=["repo", "discussion"],
    secret="my-secret",
    disabled=True,
)
download_bucket_files
<
source
>
( bucket_id: strfiles: list[tuple[str | BucketFile, str | Path]]raise_on_missing_files: bool = Falsetoken: str | bool | None = None )

Parameters

bucket_id (str) — The ID of the bucket (e.g. "username/my-bucket").
files (list[tuple[Union[str, BucketFile], Union[str, Path]]]) — Files to download as a list of tuple (source, destination). See description above for format details.
raise_on_missing_files (bool, optional) — If True, raise an EntryNotFoundError when a requested file does not exist in the bucket. If False (default), missing files are skipped with a warning.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Download files from a bucket.

Files input is a list of (remote file, local file) tuples where remote file is either the path of the file in the bucket or a BucketFile object, and local file is the destination path on the local filesystem. When passing a BucketFile object (obtained from list_bucket_tree()), the method will skip the metadata fetching step and directly download the files.

Example:

Copied
from huggingface_hub import download_bucket_files

download_bucket_files(
    bucket_id="username/my-bucket",
    files=[
        ("models/model.safetensors", "./local/model.safetensors"),
        ("config.json", "./local/config.json"),
    ],
)
Copied
from huggingface_hub import download_bucket_files

parquet_files = [file for file in list_bucket_tree(bucket_id="username/my-bucket") if file.path.endswith(".parquet")]
download_bucket_files(
    bucket_id="username/my-bucket",
    files=[(file, f"./local/{file.path}") for file in parquet_files],
)
duplicate_repo
<
source
>
( from_id: strto_id: str | None = Nonerepo_type: str | None = Noneprivate: bool | None = Nonevisibility: RepoVisibility_T | None = Nonetoken: bool | str | None = Noneexist_ok: bool = Falsespace_hardware: SpaceHardware | None = Nonespace_storage: SpaceStorage | None = Nonespace_sleep_time: int | None = Nonespace_secrets: list[dict[str, str]] | None = Nonespace_variables: list[dict[str, str]] | None = Nonespace_volumes: list[Volume] | None = None ) → RepoUrl

Expand 13 parameters
Parameters

from_id (str) — ID of the repo to duplicate. Example: "openai/gdpval".
to_id (str, optional) — ID of the new repo. Example: "myorg/my-gdpval". If not provided, the new repo will have the same name as the original repo, but in your account.
repo_type (str, optional) — Set to "dataset" or "space" if duplicating a dataset or Space, None or "model" if duplicating a model. Default is None.
private (bool, optional) — Whether the new repo should be private or not. Defaults to the same privacy as the original repo. Cannot be passed together with visibility.
visibility (Literal["public", "private", "protected"], optional) — Visibility of the new repo. Can be "public" or "private", or "protected" for Spaces. Defaults to the same visibility as the original repo.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
exist_ok (bool, optional, defaults to False) — If True, do not raise an error if repo already exists.
space_hardware (SpaceHardware or str, optional) — Choice of Hardware if repo_type is “space”. Example: "t4-medium". See SpaceHardware for a complete list.
space_storage (SpaceStorage or str, optional) — set_space_volumes instead> Choice of persistent storage tier if repo_type is “space”. Example: "small". See SpaceStorage for a complete list.
space_sleep_time (int, optional) — Number of seconds of inactivity to wait before a Space is put to sleep. Set to -1 if you don’t want your Space to sleep (default behavior for upgraded hardware). For free hardware, you can’t configure the sleep time (value is fixed to 48 hours of inactivity). Only applicable if repo_type is “space”. See https://huggingface.co/docs/hub/spaces-gpus#sleep-time for more details.
space_secrets (list[dict[str, str]], optional) — A list of secret keys to set in your Space. Each item is in the form {"key": ..., "value": ..., "description": ...} where description is optional. Only applicable if repo_type is “space”. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets.
space_variables (list[dict[str, str]], optional) — A list of public environment variables to set in your Space. Each item is in the form {"key": ..., "value": ..., "description": ...} where description is optional. Only applicable if repo_type is “space”. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets-and-environment-variables.
space_volumes (list[Volume], optional) — A list of Volume objects to mount in the Space at duplication time. Each volume has a type ("bucket", "model", "dataset", or "space"), a source (repo or bucket ID), a mount_path (path inside the container), and optional revision, read_only, and path fields. Only applicable if repo_type is “space”.
Returns

RepoUrl

URL to the newly created repo. Value is a subclass of str containing attributes like endpoint, repo_type and repo_id.


Raises

RepositoryNotFoundError or HfHubHTTPError

RepositoryNotFoundError — If one of from_id or to_id cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
HfHubHTTPError — If the HuggingFace API returned an error

Duplicate a repo on the Hub (model, dataset, or Space).

This performs a server-side copy that preserves full git history and LFS objects without requiring a local download/upload round-trip.

Example:

Copied
from huggingface_hub import duplicate_repo

# Duplicate a model to your account
duplicate_repo("google/gemma-7b")
RepoUrl('https://huggingface.co/nateraw/gemma-7b',...)

# Duplicate a dataset with a custom name
duplicate_repo("openai/gdpval", to_id="myorg/my-gdpval", repo_type="dataset")
RepoUrl('https://huggingface.co/datasets/myorg/my-gdpval',...)

# Duplicate a Space with custom hardware
duplicate_repo("multimodalart/dreambooth-training", repo_type="space", space_hardware="t4-medium")
RepoUrl('https://huggingface.co/spaces/nateraw/dreambooth-training',...)
duplicate_space
<
source
>
( from_id: strto_id: str | None = Noneprivate: bool | None = Nonevisibility: RepoVisibility_T | None = Nonetoken: bool | str | None = Noneexist_ok: bool = Falsehardware: SpaceHardware | None = Nonestorage: SpaceStorage | None = Nonesleep_time: int | None = Nonesecrets: list[dict[str, str]] | None = Nonevariables: list[dict[str, str]] | None = None ) → RepoUrl

Expand 11 parameters
Parameters

from_id (str) — ID of the Space to duplicate. Example: "pharma/CLIP-Interrogator".
to_id (str, optional) — ID of the new Space. Example: "dog/CLIP-Interrogator". If not provided, the new Space will have the same name as the original Space, but in your account.
private (bool, optional) — Whether the new Space should be private or not. Defaults to the same privacy as the original Space. Cannot be passed together with visibility.
visibility (Literal["public", "private", "protected"], optional) — Visibility of the new Space. Can be "public", "private", or "protected". Defaults to the same visibility as the original Space.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
exist_ok (bool, optional, defaults to False) — If True, do not raise an error if repo already exists.
hardware (SpaceHardware or str, optional) — Choice of Hardware. Example: "t4-medium". See SpaceHardware for a complete list.
storage (SpaceStorage or str, optional) — Choice of persistent storage tier. Example: "small". See SpaceStorage for a complete list.
sleep_time (int, optional) — Number of seconds of inactivity to wait before a Space is put to sleep. Set to -1 if you don’t want your Space to sleep (default behavior for upgraded hardware). For free hardware, you can’t configure the sleep time (value is fixed to 48 hours of inactivity). See https://huggingface.co/docs/hub/spaces-gpus#sleep-time for more details.
secrets (list[dict[str, str]], optional) — A list of secret keys to set in your Space. Each item is in the form {"key": ..., "value": ..., "description": ...} where description is optional. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets.
variables (list[dict[str, str]], optional) — A list of public environment variables to set in your Space. Each item is in the form {"key": ..., "value": ..., "description": ...} where description is optional. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets-and-environment-variables.
Returns

RepoUrl

URL to the newly created repo. Value is a subclass of str containing attributes like endpoint, repo_type and repo_id.


Raises

RepositoryNotFoundError or HfHubHTTPError

RepositoryNotFoundError — If one of from_id or to_id cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
HfHubHTTPError — If the HuggingFace API returned an error

Duplicate a Space.

Programmatically duplicate a Space. The new Space will be created in your account and will be in the same state as the original Space (running or paused). You can duplicate a Space no matter the current state of a Space.

Example:

Copied
from huggingface_hub import duplicate_space

# Duplicate a Space to your account
duplicate_space("multimodalart/dreambooth-training")
RepoUrl('https://huggingface.co/spaces/nateraw/dreambooth-training',...)

# Can set custom destination id and visibility flag.
duplicate_space("multimodalart/dreambooth-training", to_id="my-dreambooth", visibility="private")
RepoUrl('https://huggingface.co/spaces/nateraw/my-dreambooth',...)
duplicate_space is deprecated and will be removed in version 2.0. Use duplicate_repo() instead.

edit_discussion_comment
<
source
>
( repo_id: strdiscussion_num: intcomment_id: strnew_content: strtoken: bool | str | None = Nonerepo_type: str | None = None ) → DiscussionComment

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
discussion_num (int) — The number of the Discussion or Pull Request . Must be a strictly positive integer.
comment_id (str) — The ID of the comment to edit.
new_content (str) — The new content of the comment. Comments support markdown formatting.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

DiscussionComment

the edited comment


Edits a comment on a Discussion / Pull Request.

Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
enable_space_dev_mode
<
source
>
( repo_id: strtoken: bool | str | None = None ) → SpaceRuntime

Expand 2 parameters
Parameters

repo_id (str) — ID of the Space to enable dev mode. Example: "Salesforce/BLIP2".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SpaceRuntime

Runtime information about your Space.


Raises

RepositoryNotFoundError or HfHubHTTPError or BadRequestError

RepositoryNotFoundError — If your Space is not found (error 404). Most probably wrong repo_id or your space is private but you are not authenticated.
HfHubHTTPError — 403 Forbidden: only the owner of a Space can set dev mode. If you want to handle a Space that you don’t own, either ask the owner by opening a Discussion or duplicate the Space.
BadRequestError — If your Space is a static Space. Static Spaces are always running and never billed. If you want to hide a static Space, you can set it to private.

Enable dev mode on a Space.

Spaces Dev Mode eases the debugging of your application and makes iterating on Spaces faster by allowing you to restart your application without stopping the Space container itself. This feature is available as part of a PRO or Team & Enterprise plan. See https://huggingface.co/docs/hub/spaces-dev-mode for more details.

enable_webhook
<
source
>
( webhook_id: strtoken: bool | str | None = None ) → WebhookInfo

Parameters

webhook_id (str) — The unique identifier of the webhook to enable.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

WebhookInfo

Info about the enabled webhook.


Enable a webhook (makes it “active”).

Example:

Copied
from huggingface_hub import enable_webhook
enabled_webhook = enable_webhook("654bbbc16f2ec14d77f109cc")
enabled_webhook
WebhookInfo(
    id="654bbbc16f2ec14d77f109cc",
    job=None,
    url="https://webhook.site/a2176e82-5720-43ee-9e06-f91cb4c91548",
    watched=[WebhookWatchedItem(type="user", name="julien-c"), WebhookWatchedItem(type="org", name="HuggingFaceH4")],
    domains=["repo", "discussion"],
    secret="my-secret",
    disabled=False,
)
fetch_job_logs
<
source
>
( job_id: strnamespace: str | None = Nonefollow: bool = Falsetail: int | None = Nonetoken: bool | str | None = None )

Parameters

job_id (str) — ID of the Job.
namespace (str, optional) — The namespace where the Job is running. Defaults to the current user’s namespace.
follow (bool, optional) — If True, stream logs in real-time until the job completes (blocking). If False (default), fetch only the currently available logs and return immediately (non-blocking).
tail (int, optional) — Maximum number of lines to return from the logs. When combined with follow=True, starts from the last N lines and continues streaming new logs. When follow=False, returns only the last N lines from currently available logs.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Fetch all the logs from a compute Job on Hugging Face infrastructure.

Example:

Copied
from huggingface_hub import fetch_job_logs, run_job
job = run_job(image="python:3.12", command=["python", "-c" ,"print('Hello from HF compute!')"])
for log in fetch_job_logs(job_id=job.id):
    print(log)
Hello from HF compute!

# Non-blocking: fetch only currently available logs
for log in fetch_job_logs(job_id=job.id, follow=False):
    print(log)

# Stream logs starting from the last 100 lines
for log in fetch_job_logs(job_id=job.id, follow=True, tail=100):
    print(log)
fetch_job_metrics
<
source
>
( job_id: strnamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

job_id (str) — ID of the Job.
namespace (str, optional) — The namespace where the Job is running. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Fetch all the live metrics from a compute Job on Hugging Face infrastructure.

Example:

Copied
from huggingface_hub import fetch_job_metrics, run_job
job = run_job(image="python:3.12", command=["python", "-c" ,"print('Hello from HF compute!')"], flavor="a10g-small")
for metrics in fetch_job_metrics(job_id=job.id):
    print(metrics)
{
    "cpu_usage_pct": 0,
    "cpu_millicores": 3500,
    "memory_used_bytes": 1306624,
    "memory_total_bytes": 15032385536,
    "rx_bps": 0,
    "tx_bps": 0,
    "gpus": {
        "882fa930": {
            "utilization": 0,
            "memory_used_bytes": 0,
            "memory_total_bytes": 22836000000
        }
    },
    "replica": "57vr7"
}
fetch_space_logs
<
source
>
( repo_id: strbuild: bool = Falsefollow: bool = Falsetoken: bool | str | None = None ) → Iterable[str]

Parameters

repo_id (str) — ID of the Space. Example: "bigcode/in-the-stack".
build (bool, optional, defaults to False) — If True, fetch the container build logs (useful when a Space is stuck in BUILD_ERROR). If False (default), fetch the run logs, i.e. the stdout/stderr of the running application.
follow (bool, optional, defaults to False) — If True, stream logs in real-time (blocking) until the server closes the stream or KeyboardInterrupt is raised. If False (default), fetch only the currently buffered logs and return immediately (non-blocking, like docker logs).
token (bool or str, optional) — A valid user access token. Defaults to the locally saved token, which is the recommended authentication method. Set to False to disable authentication. See https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Returns

Iterable[str]

A generator yielding log lines as they become available.


Fetch the run or build logs of a Space on the Hub.

Useful for debugging a Space that is failing to build or crashing at runtime, especially from a script or agentic workflow where reading logs in a browser is not an option.

Example:

Copied
from huggingface_hub import fetch_space_logs
# Non-blocking: print currently available run logs and exit.
for line in fetch_space_logs("username/my-space"):
    print(line, end="")

# Debug a build failure:
for line in fetch_space_logs("username/my-space", build=True):
    print(line, end="")

# Stream run logs until the server closes the stream.
for line in fetch_space_logs("username/my-space", follow=True):
    print(line, end="")
file_exists
<
source
>
( repo_id: strfilename: strrepo_type: str | None = Nonerevision: str | None = Nonetoken: str | bool | None = None )

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
filename (str) — The name of the file to check, for example: "config.json"
repo_type (str, optional) — Set to "dataset" or "space" if getting repository info from a dataset or a space, None or "model" if getting repository info from a model. Default is None.
revision (str, optional) — The revision of the repository from which to get the information. Defaults to "main" branch.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Checks if a file exists in a repository on the Hugging Face Hub.

Examples:

Copied
from huggingface_hub import file_exists
file_exists("bigcode/starcoder", "config.json")
True
file_exists("bigcode/starcoder", "not-a-file")
False
file_exists("bigcode/not-a-repo", "config.json")
False
get_bucket_file_metadata
<
source
>
( bucket_id: strremote_path: strtoken: str | bool | None = None ) → BucketFileMetadata

Parameters

bucket_id (str) — The ID of the bucket (e.g. "username/my-bucket").
remote_path (str) — The path of the file in the bucket.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

BucketFileMetadata

The file metadata containing size and xet information.


Fetch metadata of a file in a bucket.

Example:

Copied
from huggingface_hub import get_bucket_file_metadata
metadata = get_bucket_file_metadata(
    bucket_id="username/my-bucket",
    remote_path="models/model.safetensors",
)
metadata.size
42000
get_bucket_paths_info
<
source
>
( bucket_id: strpaths: Iterable[str]token: str | bool | None = None ) → Iterable[BucketFile]

Parameters

bucket_id (str) — The ID of the bucket (e.g. "username/my-bucket").
paths (Iterable[str]) — The paths to get information about. If a path does not exist, it is ignored without raising an exception. Only file paths are supported.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[BucketFile]

The information about the paths, as an iterable of BucketFile objects.


Get information about a bucket’s paths.

Calls are made in batches of 1000 paths. Results are yielded as they are received.

Example:

Copied
from huggingface_hub import get_bucket_paths_info
paths_info = get_bucket_paths_info("username/my-bucket", ["file.txt", "checkpoints/model.safetensors"])
for info in paths_info:
    print(info)
BucketFile(type='file', path='file.txt', size=2379, xet_hash='96e637d9665bd35477b1908a23f2e254edfba0618dbd2d62f90a6baee7d139cf', mtime=datetime.datetime(2024, 9, 25, 15, 31, 2, 346000, tzinfo=datetime.timezone.utc))
BucketFile(type='file', path='checkpoints/model.safetensors', size=2408828, xet_hash='3ed0e9fefe788ddd61d1e26eba67057e9740a064b009256fbafadf6bb95785ca', mtime=datetime.datetime(2024, 9, 25, 15, 31, 2, 346000, tzinfo=datetime.timezone.utc))
get_collection
<
source
>
( collection_slug: strtoken: bool | str | None = None )

Parameters

collection_slug (str) — Slug of the collection of the Hub. Example: "TheBloke/recent-models-64f9a55bb3115b4f513ec026".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Gets information about a Collection on the Hub.

Returns: Collection

Example:

Copied
from huggingface_hub import get_collection
collection = get_collection("TheBloke/recent-models-64f9a55bb3115b4f513ec026")
collection.title
'Recent models'
len(collection.items)
37
collection.items[0]
CollectionItem(
    item_object_id='651446103cd773a050bf64c2',
    item_id='TheBloke/U-Amethyst-20B-AWQ',
    item_type='model',
    position=88,
    note=None
)
get_dataset_leaderboard
<
source
>
( repo_id: strtoken: bool | str | None = Nonetimeout: float | None = None ) → list[DatasetLeaderboardEntry]

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /. For example: "allenai/olmOCR-bench".
token (bool or str, optional) — A valid user access token. Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
timeout (float, optional) — Whether to set a timeout for the request to the Hub.
Returns

list[DatasetLeaderboardEntry]

A list of DatasetLeaderboardEntry objects representing the leaderboard entries, sorted by rank.


Get the leaderboard for a dataset on the Hub.

The leaderboard ranks models based on their evaluation scores on the given benchmark dataset. Not all datasets have leaderboards — only benchmark datasets with evaluation results submitted to them. This gives a dataset-centric view of scores; for a model-centric view, use model_info() with expand=["evalResults"].

Raises the following errors:

RepositoryNotFoundError If the repository cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
HfHubHTTPError If the dataset does not have a leaderboard.
Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
leaderboard = api.get_dataset_leaderboard("allenai/olmOCR-bench")
leaderboard[0].model_id
'datalab-to/chandra-ocr-2'
leaderboard[0].rank
1
get_dataset_tags
<
source
>
( )

List all valid dataset tags as a nested namespace object.

get_discussion_details
<
source
>
( repo_id: strdiscussion_num: intrepo_type: str | None = Nonetoken: bool | str | None = None )

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
discussion_num (int) — The number of the Discussion or Pull Request . Must be a strictly positive integer.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Fetches a Discussion’s / Pull Request ‘s details from the Hub.

Returns: DiscussionWithDetails

Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
get_full_repo_name
<
source
>
( model_id: strorganization: str | None = Nonetoken: bool | str | None = None ) → str

Parameters

model_id (str) — The name of the model.
organization (str, optional) — If passed, the repository name will be in the organization namespace instead of the user namespace.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

str

The repository name in the user’s namespace ({username}/{model_id}) if no organization is passed, and under the organization namespace ({organization}/{model_id}) otherwise.


Returns the repository name for a given model ID and optional organization.

get_hf_file_metadata
<
source
>
( url: strtoken: bool | str | None = Nonetimeout: float | None = 10 )

Parameters

url (str) — File url, for example returned by hf_hub_url().
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
timeout (float, optional, defaults to 10) — How many seconds to wait for the server to send metadata before giving up.
Fetch metadata of a file versioned on the Hub for a given url.

get_inference_endpoint
<
source
>
( name: strnamespace: str | None = Nonetoken: bool | str | None = None ) → InferenceEndpoint

Parameters

name (str) — The name of the Inference Endpoint to retrieve information about.
namespace (str, optional) — The namespace in which the Inference Endpoint is located. Defaults to the current user.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

InferenceEndpoint

information about the requested Inference Endpoint.


Get information about an Inference Endpoint.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
endpoint = api.get_inference_endpoint("my-text-to-image")
endpoint
InferenceEndpoint(name='my-text-to-image', ...)

# Get status
endpoint.status
'running'
endpoint.url
'https://my-text-to-image.region.vendor.endpoints.huggingface.cloud'

# Run inference
endpoint.client.text_to_image(...)
get_model_tags
<
source
>
( )

List all valid model tags as a nested namespace object

get_organization_overview
<
source
>
( organization: strtoken: bool | str | None = None ) → Organization

Parameters

organization (str) — Name of the organization to get an overview of.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Organization

An Organization object with the organization’s overview.


Raises

HTTPError

HTTPError — HTTP 404 If the organization does not exist on the Hub.

Get an overview of an organization on the Hub.

get_paths_info
<
source
>
( repo_id: strpaths: list[str] | strexpand: bool = Falserevision: str | None = Nonerepo_type: str | None = Nonetoken: str | bool | None = None ) → list[Union[RepoFile, RepoFolder]]

Expand 6 parameters
Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
paths (Union[list[str], str], optional) — The paths to get information about. If a path do not exist, it is ignored without raising an exception.
expand (bool, optional, defaults to False) — Whether to fetch more information about the paths (e.g. last commit and files’ security scan results). This operation is more expensive for the server so only 50 results are returned per page (instead of 1000). As pagination is implemented in huggingface_hub, this is transparent for you except for the time it takes to get the results.
revision (str, optional) — The revision of the repository from which to get the information. Defaults to "main" branch.
repo_type (str, optional) — The type of the repository from which to get the information ("model", "dataset" or "space". Defaults to "model".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

list[Union[RepoFile, RepoFolder]]

The information about the paths, as a list of RepoFile and RepoFolder objects.


Raises

RepositoryNotFoundError or RevisionNotFoundError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.
RevisionNotFoundError — If revision is not found (error 404) on the repo.

Get information about a repo’s paths.

Example:

Copied
from huggingface_hub import get_paths_info
paths_info = get_paths_info("allenai/c4", ["README.md", "en"], repo_type="dataset")
paths_info
[
    RepoFile(path='README.md', size=2379, blob_id='f84cb4c97182890fc1dbdeaf1a6a468fd27b4fff', lfs=None, last_commit=None, security=None),
    RepoFolder(path='en', tree_id='dc943c4c40f53d02b31ced1defa7e5f438d5862e', last_commit=None)
]
get_repo_discussions
<
source
>
( repo_id: strauthor: str | None = Nonediscussion_type: constants.DiscussionTypeFilter | None = Nonediscussion_status: constants.DiscussionStatusFilter | None = Nonerepo_type: str | None = Nonetoken: bool | str | None = None ) → Iterator[Discussion]

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
author (str, optional) — Pass a value to filter by discussion author. None means no filter. Default is None.
discussion_type (str, optional) — Set to "pull_request" to fetch only pull requests, "discussion" to fetch only discussions. Set to "all" or None to fetch both. Default is None.
discussion_status (str, optional) — Set to "open" (respectively "closed") to fetch only open (respectively closed) discussions. Set to "all" or None to fetch both. Default is None.
repo_type (str, optional) — Set to "dataset" or "space" if fetching from a dataset or space, None or "model" if fetching from a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterator[Discussion]

An iterator of Discussion objects.


Fetches Discussions and Pull Requests for the given repo.

Example:

Collecting all discussions of a repo in a list:

Copied
from huggingface_hub import get_repo_discussions
discussions_list = list(get_repo_discussions(repo_id="bert-base-uncased"))
Iterating over discussions of a repo:

Copied
from huggingface_hub import get_repo_discussions
for discussion in get_repo_discussions(repo_id="bert-base-uncased"):
    print(discussion.num, discussion.title)
get_safetensors_metadata
<
source
>
( repo_id: strrepo_type: str | None = Nonerevision: str | None = Nonetoken: bool | str | None = None ) → SafetensorsRepoMetadata

Expand 4 parameters
Parameters

repo_id (str) — A user or an organization name and a repo name separated by a /.
repo_type (str, optional) — Set to "dataset" or "space" if the file is in a dataset or space, None or "model" if in a model. Default is None.
revision (str, optional) — The git revision to fetch the file from. Can be a branch name, a tag, or a commit hash. Defaults to the head of the "main" branch.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SafetensorsRepoMetadata

information related to safetensors repo.


Raises

NotASafetensorsRepoError or SafetensorsParsingError

NotASafetensorsRepoError — If the repo is not a safetensors repo i.e. doesn’t have either a model.safetensors or a model.safetensors.index.json file.
SafetensorsParsingError — If a safetensors file header couldn’t be parsed correctly.

Parse metadata for a safetensors repo on the Hub.

We first check if the repo has a single safetensors file or a sharded safetensors repo. If it’s a single safetensors file, we parse the metadata from this file. If it’s a sharded safetensors repo, we parse the metadata from the index file and then parse the metadata from each shard.

To parse metadata from a single safetensors file, use parse_safetensors_file_metadata().

For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

Example:

Copied
# Parse repo with single weights file
metadata = get_safetensors_metadata("bigscience/bloomz-560m")
metadata
SafetensorsRepoMetadata(
    metadata=None,
    sharded=False,
    weight_map={'h.0.input_layernorm.bias': 'model.safetensors', ...},
    files_metadata={'model.safetensors': SafetensorsFileMetadata(...)}
)
metadata.files_metadata["model.safetensors"].metadata
{'format': 'pt'}

# Parse repo with sharded model
metadata = get_safetensors_metadata("bigscience/bloom")
Parse safetensors files: 100%|██████████████████████████████████████████| 72/72 [00:12<00:00,  5.78it/s]
metadata
SafetensorsRepoMetadata(metadata={'total_size': 352494542848}, sharded=True, weight_map={...}, files_metadata={...})
len(metadata.files_metadata)
72  # All safetensors files have been fetched

# Parse repo with sharded model
get_safetensors_metadata("runwayml/stable-diffusion-v1-5")
NotASafetensorsRepoError: 'runwayml/stable-diffusion-v1-5' is not a safetensors repo. Couldn't find 'model.safetensors.index.json' or 'model.safetensors' files.
get_space_runtime
<
source
>
( repo_id: strtoken: bool | str | None = None ) → SpaceRuntime

Parameters

repo_id (str) — ID of the repo to update. Example: "bigcode/in-the-stack".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SpaceRuntime

Runtime information about a Space including Space stage and hardware.


Gets runtime information about a Space.

get_space_secrets
<
source
>
( repo_id: strtoken: bool | str | None = None ) → dict[str, SpaceSecret]

Parameters

repo_id (str) — ID of the repo to query. Example: "bigcode/in-the-stack".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

dict[str, SpaceSecret]

Dictionary of SpaceSecret objects keyed by secret name.


Gets all secrets from a Space.

Secret values are write-only and cannot be read back. Only the key, description, and last update time are returned.

Secrets allow to set secret keys or tokens to a Space without hardcoding them. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
api.get_space_secrets("username/my-space")
{'HF_TOKEN': SpaceSecret(key='HF_TOKEN', description='...', updated_at=datetime.datetime(...))}
get_space_variables
<
source
>
( repo_id: strtoken: bool | str | None = None )

Parameters

repo_id (str) — ID of the repo to query. Example: "bigcode/in-the-stack".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Gets all variables from a Space.

Variables allow to set environment variables to a Space without hardcoding them. For more details, see https://huggingface.co/docs/hub/spaces-overview#managing-secrets-and-environment-variables

get_user_overview
<
source
>
( username: strtoken: bool | str | None = None ) → User

Parameters

username (str) — Username of the user to get an overview of.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

User

A User object with the user’s overview.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 404 If the user does not exist on the Hub.

Get an overview of a user on the Hub.

get_webhook
<
source
>
( webhook_id: strtoken: bool | str | None = None ) → WebhookInfo

Parameters

webhook_id (str) — The unique identifier of the webhook to get.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

WebhookInfo

Info about the webhook.


Get a webhook by its id.

Example:

Copied
from huggingface_hub import get_webhook
webhook = get_webhook("654bbbc16f2ec14d77f109cc")
print(webhook)
WebhookInfo(
    id="654bbbc16f2ec14d77f109cc",
    job=None,
    watched=[WebhookWatchedItem(type="user", name="julien-c"), WebhookWatchedItem(type="org", name="HuggingFaceH4")],
    url="https://webhook.site/a2176e82-5720-43ee-9e06-f91cb4c91548",
    secret="my-secret",
    domains=["repo", "discussion"],
    disabled=False,
)
grant_access
<
source
>
( repo_id: struser: strrepo_type: str | None = Nonetoken: bool | str | None = None )

Parameters

repo_id (str) — The id of the repo to grant access to.
user (str) — The username of the user to grant access.
repo_type (str, optional) — The type of the repo to grant access to. Must be one of model, dataset or space. Defaults to model.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

HfHubHTTPError

HfHubHTTPError — HTTP 400 if the repo is not gated.
HfHubHTTPError — HTTP 400 if the user already has access to the repo.
HfHubHTTPError — HTTP 403 if you only have read-only access to the repo. This can be the case if you don’t have write or admin role in the organization the repo belongs to or if you passed a read token.
HfHubHTTPError — HTTP 404 if the user does not exist on the Hub.

Grant access to a user for a given gated repo.

Granting access don’t require for the user to send an access request by themselves. The user is automatically added to the accepted list meaning they can download the files You can revoke the granted access at any time using cancel_access_request() or reject_access_request().

For more info about gated repos, see https://huggingface.co/docs/hub/models-gated.

hf_hub_download
<
source
>
( repo_id: strfilename: strsubfolder: str | None = Nonerepo_type: str | None = Nonerevision: str | None = Nonecache_dir: str | Path | None = Nonelocal_dir: str | Path | None = Noneforce_download: bool = Falseetag_timeout: float = 10token: bool | str | None = Nonelocal_files_only: bool = Falsetqdm_class: type[base_tqdm] | None = Nonedry_run: bool = False ) → str or DryRunFileInfo

Expand 13 parameters
Parameters

repo_id (str) — A user or an organization name and a repo name separated by a /.
filename (str) — The name of the file in the repo.
subfolder (str, optional) — An optional value corresponding to a folder inside the repository.
repo_type (str, optional) — Set to "dataset" or "space" if downloading from a dataset or space, None or "model" if downloading from a model. Default is None.
revision (str, optional) — An optional Git revision id which can be a branch name, a tag, or a commit hash.
cache_dir (str, Path, optional) — Path to the folder where cached files are stored.
local_dir (str or Path, optional) — If provided, the downloaded file will be placed under this directory.
force_download (bool, optional, defaults to False) — Whether the file should be downloaded even if it already exists in the local cache.
etag_timeout (float, optional, defaults to 10) — When fetching ETag, how many seconds to wait for the server to send data before giving up which is passed to httpx.request.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
local_files_only (bool, optional, defaults to False) — If True, avoid downloading the file and return the path to the local cached file if it exists.
tqdm_class (tqdm, optional) — If provided, overwrites the default behavior for the progress bar. Passed argument must inherit from tqdm.auto.tqdm or at least mimic its behavior. Defaults to the custom HF progress bar that can be disabled by setting HF_HUB_DISABLE_PROGRESS_BARS environment variable.
dry_run (bool, optional, defaults to False) — If True, perform a dry run without actually downloading the file. Returns a DryRunFileInfo object containing information about what would be downloaded.
Returns

str or DryRunFileInfo

If dry_run=False: Local path of file or if networking is off, last version of file cached on disk.
If dry_run=True: A DryRunFileInfo object containing download information.

Raises

RepositoryNotFoundError or RevisionNotFoundError or ~utils.RemoteEntryNotFoundError or LocalEntryNotFoundError or EnvironmentError or OSError or ValueError

RepositoryNotFoundError — If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
RevisionNotFoundError — If the revision to download from cannot be found.
~utils.RemoteEntryNotFoundError — If the file to download cannot be found.
LocalEntryNotFoundError — If network is disabled or unavailable and file is not found in cache.
EnvironmentError — If token=True but the token cannot be found.
OSError — If ETag cannot be determined.
ValueError — If some parameter value is invalid.

Download a given file if it’s not already present in the local cache.

The new cache file layout looks like this:

The cache directory contains one subfolder per repo_id (namespaced by repo type)
inside each repo folder:
refs is a list of the latest known revision => commit_hash pairs
blobs contains the actual file blobs (identified by their git-sha or sha256, depending on whether they’re LFS files or not)
snapshots contains one subfolder per commit, each “commit” contains the subset of the files that have been resolved at that particular commit. Each filename is a symlink to the blob at that particular commit.
Copied
[  96]  .
└── [ 160]  models--julien-c--EsperBERTo-small
    ├── [ 160]  blobs
    │   ├── [321M]  403450e234d65943a7dcf7e05a771ce3c92faa84dd07db4ac20f592037a1e4bd
    │   ├── [ 398]  7cb18dc9bafbfcf74629a4b760af1b160957a83e
    │   └── [1.4K]  d7edf6bd2a681fb0175f7735299831ee1b22b812
    ├── [  96]  refs
    │   └── [  40]  main
    └── [ 128]  snapshots
        ├── [ 128]  2439f60ef33a0d46d85da5001d52aeda5b00ce9f
        │   ├── [  52]  README.md -> ../../blobs/d7edf6bd2a681fb0175f7735299831ee1b22b812
        │   └── [  76]  pytorch_model.bin -> ../../blobs/403450e234d65943a7dcf7e05a771ce3c92faa84dd07db4ac20f592037a1e4bd
        └── [ 128]  bbc77c8132af1cc5cf678da3f1ddf2de43606d48
            ├── [  52]  README.md -> ../../blobs/7cb18dc9bafbfcf74629a4b760af1b160957a83e
            └── [  76]  pytorch_model.bin -> ../../blobs/403450e234d65943a7dcf7e05a771ce3c92faa84dd07db4ac20f592037a1e4bd
If local_dir is provided, the file structure from the repo will be replicated in this location. When using this option, the cache_dir will not be used and a .cache/huggingface/ folder will be created at the root of local_dir to store some metadata related to the downloaded files. While this mechanism is not as robust as the main cache-system, it’s optimized for regularly pulling the latest version of a repository.

hide_discussion_comment
<
source
>
( repo_id: strdiscussion_num: intcomment_id: strtoken: bool | str | None = Nonerepo_type: str | None = None ) → DiscussionComment

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
discussion_num (int) — The number of the Discussion or Pull Request . Must be a strictly positive integer.
comment_id (str) — The ID of the comment to edit.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

DiscussionComment

the hidden comment


Hides a comment on a Discussion / Pull Request.

Hidden comments’ content cannot be retrieved anymore. Hiding a comment is irreversible.

Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
inspect_job
<
source
>
( job_id: strnamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

job_id (str) — ID of the Job.
namespace (str, optional) — The namespace where the Job is running. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Inspect a compute Job on Hugging Face infrastructure.

Example:

Copied
from huggingface_hub import inspect_job, run_job
job = run_job(image="python:3.12", command=["python", "-c" ,"print('Hello from HF compute!')"])
inspect_job(job.id)
JobInfo(
    id='68780d00bbe36d38803f645f',
    created_at=datetime.datetime(2025, 7, 16, 20, 35, 12, 808000, tzinfo=datetime.timezone.utc),
    docker_image='python:3.12',
    space_id=None,
    command=['python', '-c', "print('Hello from HF compute!')"],
    arguments=[],
    environment={},
    secrets={},
    flavor='cpu-basic',
    status=JobStatus(stage='RUNNING', message=None)
)
inspect_scheduled_job
<
source
>
( scheduled_job_id: strnamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

scheduled_job_id (str) — ID of the scheduled Job.
namespace (str, optional) — The namespace where the scheduled Job is. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Inspect a scheduled compute Job on Hugging Face infrastructure.

Example:

Copied
from huggingface_hub import inspect_job, create_scheduled_job
scheduled_job = create_scheduled_job(image="python:3.12", command=["python", "-c" ,"print('Hello from HF compute!')"], schedule="@hourly")
inspect_scheduled_job(scheduled_job.id)
kernel_info
<
source
>
( repo_id: strrevision: str | None = Nonetimeout: float | None = Nonetoken: bool | str | None = None ) → ModelInfo

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
revision (str, optional) — The revision of the kernel repository from which to get the information.
timeout (float, optional) — Whether to set a timeout for the request to the Hub.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

ModelInfo

The kernel repository information.


Get info on one specific kernel on huggingface.co.

list_accepted_access_requests
<
source
>
( repo_id: strrepo_type: str | None = Nonetoken: bool | str | None = None ) → Iterable[AccessRequest]

Expand 3 parameters
Parameters

repo_id (str) — The id of the repo to get access requests for.
repo_type (str, optional) — The type of the repo to get access requests for. Must be one of model, dataset or space. Defaults to model.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[AccessRequest]

An iterable of AccessRequest objects. Each time contains a username, email, status and timestamp attribute. If the gated repo has a custom form, the fields attribute will be populated with user’s answers.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 400 if the repo is not gated.
HfHubHTTPError — HTTP 403 if you only have read-only access to the repo. This can be the case if you don’t have write or admin role in the organization the repo belongs to or if you passed a read token.

Get accepted access requests for a given gated repo.

An accepted request means the user has requested access to the repo and the request has been accepted. The user can download any file of the repo. If the approval mode is automatic, this list should contains by default all requests. Accepted requests can be cancelled or rejected at any time using cancel_access_request() and reject_access_request(). A cancelled request will go back to the pending list while a rejected request will go to the rejected list. In both cases, the user will lose access to the repo.

For more info about gated repos, see https://huggingface.co/docs/hub/models-gated.

Example:

Copied
from huggingface_hub import list_accepted_access_requests

requests = list(list_accepted_access_requests("meta-llama/Llama-2-7b"))
len(requests)
411
requests[0]
[
    AccessRequest(
        username='clem',
        fullname='Clem 🤗',
        email='***',
        timestamp=datetime.datetime(2023, 11, 23, 18, 4, 53, 828000, tzinfo=datetime.timezone.utc),
        status='accepted',
        fields=None,
    ),
    ...
]
list_bucket_tree
<
source
>
( bucket_id: strprefix: str | None = Nonerecursive: bool | None = Nonetoken: str | bool | None = None ) → Iterable[Union[BucketFile, BucketFolder]]

Parameters

bucket_id (str) — The ID of the bucket (e.g. "username/my-bucket").
prefix (str, optional) — Filter results to files whose path starts with this prefix.
recursive (bool, optional) — If True, list files recursively. If False (default), list files and directories only at root.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[Union[BucketFile, BucketFolder]]

An iterable of BucketFile and BucketFolder objects containing file and directory information (path, etc.).


List files in a bucket.

Example:

Copied
from huggingface_hub import list_bucket_tree
for file_info in list_bucket_tree(bucket_id="username/my-bucket"):
    print(file_info.path)

# Filter by prefix
for file_info in list_bucket_tree(bucket_id="username/my-bucket", prefix="models/"):
    print(file_info.path)
list_buckets
<
source
>
( namespace: str | None = Nonesearch: str | None = Nonetoken: bool | str | None = None ) → Iterable[BucketInfo]

Parameters

namespace (str, optional) — List buckets under this namespace (user or organization). Defaults to listing user’s buckets.
search (str, optional) — A search string to filter bucket names.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[BucketInfo]

An iterable of BucketInfo objects.


List buckets on the Hub under a certain namespace.

Example:

Copied
from huggingface_hub import list_buckets
for bucket in list_buckets(): # lists buckets in the user's namespace
    print(bucket)

for bucket in list_buckets(namespace="huggingface"): # lists buckets in the "huggingface" organization
    print(bucket)

for bucket in list_buckets(search="my-prefix"): # filter buckets by name
    print(bucket)
list_collections
<
source
>
( owner: list[str] | str | None = Noneitem: list[str] | str | None = Nonesort: CollectionSort_T | None = Nonelimit: int | None = Nonetoken: bool | str | None = None ) → Iterable[Collection]

Parameters

owner (list[str] or str, optional) — Filter by owner’s username.
item (list[str] or str, optional) — Filter collections containing a particular items. Example: "models/teknium/OpenHermes-2.5-Mistral-7B", "datasets/squad" or "papers/2311.12983".
sort (Literal["lastModified", "trending", "upvotes"], optional) — Sort collections by last modified, trending or upvotes.
limit (int, optional) — Maximum number of collections to be returned.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[Collection]

an iterable of Collection objects.


List collections on the Huggingface Hub, given some filters.

When listing collections, the item list per collection is truncated to 4 items maximum. To retrieve all items from a collection, you must use get_collection().

list_daily_papers
<
source
>
( date: str | None = Nonetoken: bool | str | None = Noneweek: str | None = Nonemonth: str | None = Nonesubmitter: str | None = Nonesort: DailyPapersSort_T | None = Nonep: int | None = Nonelimit: int | None = None ) → Iterable[PaperInfo]

Parameters

date (str, optional) — Date in ISO format (YYYY-MM-DD) for which to fetch daily papers. Defaults to most recent ones.
token (Union[bool, str, None], optional) — A valid user access token (string). Defaults to the locally saved token. To disable authentication, pass False.
week (str, optional) — Week in ISO format (YYYY-Www) for which to fetch daily papers. Example, 2025-W09.
month (str, optional) — Month in ISO format (YYYY-MM) for which to fetch daily papers. Example, 2025-02.
submitter (str, optional) — Username of the submitter to filter daily papers.
sort (Literal["publishedAt", "trending"], optional) — Sort order for the daily papers. Can be either by publishedAt or by trending. Defaults to "publishedAt"
p (int, optional) — Page number for pagination. Defaults to 0.
limit (int, optional) — Limit of papers to fetch. Defaults to 50.
Returns

Iterable[PaperInfo]

an iterable of huggingface_hub.hf_api.PaperInfo objects.


List the daily papers published on a given date on the Hugging Face Hub.

Example:

Copied
from huggingface_hub import HfApi

api = HfApi()
list(api.list_daily_papers(date="2025-10-29"))
list_dataset_parquet_files
<
source
>
( repo_id: strconfig: str | None = Nonetoken: bool | str | None = None ) → list[DatasetParquetEntry]

Parameters

repo_id (str) — The dataset repository ID (e.g. "username/dataset-name").
config (str, optional) — Filter by a specific config/subset name. When provided, only parquet files for that config are returned.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

list[DatasetParquetEntry]

a list of DatasetParquetEntry objects containing config, split, url and size for each parquet file.


List parquet files available for a dataset on the Hub.

All datasets hosted on the Hub are auto-converted to Parquet by the Dataset Viewer. This method returns the list of parquet files with their URLs, configs, splits and sizes.

Example:

Copied
from huggingface_hub import list_dataset_parquet_files
list_dataset_parquet_files("lhoestq/demo1")
entries[0]
DatasetParquetEntry(config='default', split='train', url='https://huggingface.co/...', size=5038)
list_datasets
<
source
>
( filter: str | Iterable[str] | None = Noneauthor: str | None = Nonebenchmark: Literal[True] | Literal['official'] | str | None = Nonedataset_name: str | None = Nonegated: bool | None = Nonelanguage_creators: str | list[str] | None = Nonelanguage: str | list[str] | None = Nonemultilinguality: str | list[str] | None = Nonesize_categories: str | list[str] | None = Nonetask_categories: str | list[str] | None = Nonetask_ids: str | list[str] | None = Nonesearch: str | None = Nonesort: DatasetSort_T | None = Nonelimit: int | None = Noneexpand: list[ExpandDatasetProperty_T] | None = Nonefull: bool | None = Nonetoken: bool | str | None = None ) → Iterable[DatasetInfo]

Expand 18 parameters
Parameters

filter (str or Iterable[str], optional) — A string or list of string to filter datasets on the hub.
author (str, optional) — A string which identify the author of the returned datasets.
benchmark (True, "official", str, optional) — Filter datasets by benchmark. Can be True or "official" to return official benchmark datasets. For future-compatibility, can also be a string representing the benchmark name (currently only “official” is supported).
dataset_name (str, optional) — A string or list of strings that can be used to identify datasets on the Hub by its name, such as SQAC or wikineural
gated (bool, optional) — A boolean to filter datasets on the Hub that are gated or not. By default, all datasets are returned. If gated=True is passed, only gated datasets are returned. If gated=False is passed, only non-gated datasets are returned.
language_creators (str or List, optional) — A string or list of strings that can be used to identify datasets on the Hub with how the data was curated, such as crowdsourced or machine_generated.
language (str or List, optional) — A string or list of strings representing a two-character language to filter datasets by on the Hub.
multilinguality (str or List, optional) — A string or list of strings representing a filter for datasets that contain multiple languages.
size_categories (str or List, optional) — A string or list of strings that can be used to identify datasets on the Hub by the size of the dataset such as 100K<n<1M or 1M<n<10M.
tags (str or List, optional) — Deprecated. Pass tags in filter to filter datasets by tags.
task_categories (str or List, optional) — A string or list of strings that can be used to identify datasets on the Hub by the designed task, such as audio_classification or named_entity_recognition.
task_ids (str or List, optional) — A string or list of strings that can be used to identify datasets on the Hub by the specific task such as speech_emotion_recognition or paraphrase.
search (str, optional) — A string that will be contained in the returned datasets.
sort (DatasetSort_T, optional) — The key with which to sort the resulting datasets. Possible values are “created_at”, “downloads”, “last_modified”, “likes” and “trending_score”.
limit (int, optional) — The limit on the number of datasets fetched. Leaving this option to None fetches all datasets.
expand (list[ExpandDatasetProperty_T], optional) — List properties to return in the response. When used, only the properties in the list will be returned. This parameter cannot be used if full is passed. Possible values are "author", "cardData", "citation", "createdAt", "disabled", "description", "downloads", "downloadsAllTime", "gated", "lastModified", "likes", "mainSize", "paperswithcode_id", "private", "siblings", "sha", "tags", "trendingScore", "usedStorage", and "resourceGroup".
full (bool, optional) — Whether to fetch all dataset data, including the last_modified, the card_data and the files. Can contain useful information such as the PapersWithCode ID.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[DatasetInfo]

an iterable of huggingface_hub.hf_api.DatasetInfo objects.


List datasets hosted on the Huggingface Hub, given some filters.

Example usage with the filter argument:

Copied
from huggingface_hub import HfApi

api = HfApi()

# List all datasets
api.list_datasets()


# List only the text classification datasets
api.list_datasets(filter="task_categories:text-classification")


# List only the datasets in russian for language modeling
api.list_datasets(
    filter=("language:ru", "task_ids:language-modeling")
)

# List FiftyOne datasets (identified by the tag "fiftyone" in dataset card)
api.list_datasets(tags="fiftyone")
Example usage with the search argument:

Copied
from huggingface_hub import HfApi

api = HfApi()

# List all datasets with "text" in their name
api.list_datasets(search="text")

# List all datasets with "text" in their name made by google
api.list_datasets(search="text", author="google")
list_inference_catalog
<
source
>
( token: bool | str | None = None ) → Liststr

Parameters

token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication).
Returns

Liststr

A list of model IDs available in the catalog.


List models available in the Hugging Face Inference Catalog.

The goal of the Inference Catalog is to provide a curated list of models that are optimized for inference and for which default configurations have been tested. See https://endpoints.huggingface.co/catalog for a list of available models in the catalog.

Use create_inference_endpoint_from_catalog() to deploy a model from the catalog.

list_inference_catalog is experimental. Its API is subject to change in the future. Please provide feedback if you have any suggestions or requests.

list_inference_endpoints
<
source
>
( namespace: str | None = Nonetoken: bool | str | None = None ) → listInferenceEndpoint

Parameters

namespace (str, optional) — The namespace to list endpoints for. Defaults to the current user. Set to "*" to list all endpoints from all namespaces (i.e. personal namespace and all orgs the user belongs to).
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

listInferenceEndpoint

A list of all inference endpoints for the given namespace.


Lists all inference endpoints for the given namespace.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
api.list_inference_endpoints()
[InferenceEndpoint(name='my-endpoint', ...), ...]
list_jobs
<
source
>
( status: list[JobStage | str] | JobStage | str | None = Nonelabels: dict[str, str] | None = Nonetimeout: int | None = Nonenamespace: str | None = Nonetoken: bool | str | None = None ) → Iterable[JobInfo]

Parameters

status (JobStage, str or list, optional) — Only return Jobs with the given status(es), e.g. "RUNNING" or [JobStage.RUNNING, JobStage.SCHEDULING]. See JobStage for possible values.
labels (dict[str, str], optional) — Only return Jobs that have all the given key=value labels, e.g. {"env": "prod", "team": "ml"}.
timeout (float, optional) — Whether to set a timeout for the request to the Hub.
namespace (str, optional) — The namespace from where it lists the jobs. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Returns

Iterable[JobInfo]

an iterable of JobInfo objects.


List compute Jobs on Hugging Face infrastructure.

list_jobs_hardware
<
source
>
( token: bool | str | None = None ) → list[JobHardwareInfo]

Returns

list[JobHardwareInfo]

A list of available hardware configurations.


List available hardware options for Jobs on Hugging Face infrastructure.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
hardware_list = api.list_jobs_hardware()
hardware_list[0]
JobHardwareInfo(name='cpu-basic', pretty_name='CPU Basic', cpu='2 vCPU', ram='16 GB', ephemeral_storage='20 GB', accelerator=None, unit_cost_micro_usd=167, unit_cost_usd=0.000167, unit_label='minute')
hardware_list[0].name
'cpu-basic'

# Filter GPU options
gpu_hardware = [hw for hw in hardware_list if hw.accelerator is not None]
gpu_hardware[0].accelerator.model
'T4'
list_lfs_files
<
source
>
( repo_id: strrepo_type: str | None = Nonetoken: bool | str | None = None ) → Iterable[LFSFileInfo]

Parameters

repo_id (str) — The repository for which you are listing LFS files.
repo_type (str, optional) — Type of repository. Set to "dataset" or "space" if listing from a dataset or space, None or "model" if listing from a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[LFSFileInfo]

An iterator of LFSFileInfo objects.


List all LFS files in a repo on the Hub.

This is primarily useful to count how much storage a repo is using and to eventually clean up large files with permanently_delete_lfs_files(). Note that this would be a permanent action that will affect all commits referencing this deleted files and that cannot be undone.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
lfs_files = api.list_lfs_files("username/my-cool-repo")

# Filter files files to delete based on a combination of `filename`, `pushed_at`, `ref` or `size`.
# e.g. select only LFS files in the "checkpoints" folder
lfs_files_to_delete = (lfs_file for lfs_file in lfs_files if lfs_file.filename.startswith("checkpoints/"))

# Permanently delete LFS files
api.permanently_delete_lfs_files("username/my-cool-repo", lfs_files_to_delete)
list_liked_repos
<
source
>
( user: str | None = Nonetoken: bool | str | None = None ) → UserLikes

Parameters

user (str, optional) — Name of the user for which you want to fetch the likes.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

UserLikes

object containing the user name and 3 lists of repo ids (1 for models, 1 for datasets and 1 for Spaces).


Raises

ValueError

ValueError — If user is not passed and no token found (either from argument or from machine).

List all public repos liked by a user on huggingface.co.

This list is public so token is optional. If user is not passed, it defaults to the logged in user.

See also unlike().

Example:

Copied
from huggingface_hub import list_liked_repos

likes = list_liked_repos("julien-c")

likes.user
"julien-c"

likes.models
["osanseviero/streamlit_1.15", "Xhaheen/ChatGPT_HF", ...]
list_models
<
source
>
( filter: str | Iterable[str] | None = Noneauthor: str | None = Noneapps: str | list[str] | None = Nonegated: bool | None = Noneinference: Literal['warm'] | None = Noneinference_provider: Literal['all'] | PROVIDER_T | list[PROVIDER_T] | None = Nonemodel_name: str | None = Nonetrained_dataset: str | list[str] | None = Nonesearch: str | None = Nonepipeline_tag: str | None = Nonenum_parameters: str | None = Noneemissions_thresholds: tuple[float, float] | None = Nonesort: ModelSort_T | None = Nonelimit: int | None = Noneexpand: list[ExpandModelProperty_T] | None = Nonefull: bool | None = NonecardData: bool = Falsefetch_config: bool = Falsetoken: bool | str | None = None ) → Iterable[ModelInfo]

Expand 19 parameters
Parameters

filter (str or Iterable[str], optional) — A string or list of string to filter models on the Hub. Models can be filtered by library, language, task, tags, and more.
author (str, optional) — A string which identify the author (user or organization) of the returned models.
apps (str or List, optional) — A string or list of strings to filter models on the Hub that support the specified apps. Example values include "ollama" or ["ollama", "vllm"].
gated (bool, optional) — A boolean to filter models on the Hub that are gated or not. By default, all models are returned. If gated=True is passed, only gated models are returned. If gated=False is passed, only non-gated models are returned.
inference (Literal["warm"], optional) — If “warm”, filter models on the Hub currently served by at least one provider.
inference_provider (Literal["all"] or str, optional) — A string to filter models on the Hub that are served by a specific provider. Pass "all" to get all models served by at least one provider.
trained_dataset (str or List, optional) — A string tag or a list of string tags of the trained dataset for a model on the Hub.
search (str, optional) — A string that will be contained in the returned model ids.
pipeline_tag (str, optional) — A string pipeline tag to filter models on the Hub by, such as summarization.
num_parameters (str, optional) — Filter models by parameter count. Accepts the same range syntax as the Hub UI and API, for example "min:6B,max:128B", "min:6B" or "max:128B".
emissions_thresholds (Tuple, optional) — A tuple of two ints or floats representing a minimum and maximum carbon footprint to filter the resulting models with in grams.
sort (ModelSort_T, optional) — The key with which to sort the resulting models. Possible values are “created_at”, “downloads”, “last_modified”, “likes” and “trending_score”.
limit (int, optional) — The limit on the number of models fetched. Leaving this option to None fetches all models.
expand (list[ExpandModelProperty_T], optional) — List properties to return in the response. When used, only the properties in the list will be returned. This parameter cannot be used if full, cardData or fetch_config are passed. Possible values are "author", "cardData", "config", "createdAt", "disabled", "downloads", "downloadsAllTime", "evalResults", "gated", "gguf", "inference", "inferenceProviderMapping", "lastModified", "library_name", "likes", "mask_token", "model-index", "pipeline_tag", "private", "safetensors", "sha", "siblings", "spaces", "tags", "transformersInfo", "trendingScore", "widgetData", and "resourceGroup".
full (bool, optional) — Whether to fetch all model data, including the last_modified, the sha, the files and the tags. This is set to True by default when using a filter.
cardData (bool, optional) — Whether to grab the metadata for the model as well. Can contain useful information such as carbon emissions, metrics, and datasets trained on.
fetch_config (bool, optional) — Whether to fetch the model configs as well. This is not included in full due to its size.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
model_name (str, optional) — (deprecated). Use search instead.
Returns

Iterable[ModelInfo]

an iterable of huggingface_hub.hf_api.ModelInfo objects.


List models hosted on the Huggingface Hub, given some filters.

Example:

Copied
from huggingface_hub import HfApi

api = HfApi()

# List all models
api.list_models()

# List text classification models
api.list_models(filter="text-classification")

# List models from the KerasHub library
api.list_models(filter="keras-hub")

# List models served by Cohere
api.list_models(inference_provider="cohere")

# List models with "bert" in their name
api.list_models(search="bert")

# List models with "bert" in their name and pushed by google
api.list_models(search="bert", author="google")

# List models with 6B to 128B parameters
api.list_models(num_parameters="min:6B,max:128B", sort="likes")
list_organization_followers
<
source
>
( organization: strtoken: bool | str | None = None ) → Iterable[User]

Parameters

organization (str) — Name of the organization to get the followers of.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[User]

A list of User objects with the followers of the organization.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 404 If the organization does not exist on the Hub.

List followers of an organization on the Hub.

list_organization_members
<
source
>
( organization: strtoken: bool | str | None = None ) → Iterable[User]

Parameters

organization (str) — Name of the organization to get the members of.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[User]

A list of User objects with the members of the organization.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 404 If the organization does not exist on the Hub.

List of members of an organization on the Hub.

list_papers
<
source
>
( query: str | None = Nonelimit: int | None = Nonetoken: bool | str | None = None ) → Iterable[PaperInfo]

Parameters

query (str, optional) — A search query string to find papers. If provided, returns papers that match the query.
limit (int, optional) — The maximum number of papers to return.
token (Union[bool, str, None], optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[PaperInfo]

an iterable of huggingface_hub.hf_api.PaperInfo objects.


List daily papers on the Hugging Face Hub given a search query.

Example:

Copied
from huggingface_hub import HfApi

api = HfApi()

# List all papers with "attention" in their title
api.list_papers(query="attention")
list_pending_access_requests
<
source
>
( repo_id: strrepo_type: str | None = Nonetoken: bool | str | None = None ) → Iterable[AccessRequest]

Expand 3 parameters
Parameters

repo_id (str) — The id of the repo to get access requests for.
repo_type (str, optional) — The type of the repo to get access requests for. Must be one of model, dataset or space. Defaults to model.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[AccessRequest]

An iterable of AccessRequest objects. Each time contains a username, email, status and timestamp attribute. If the gated repo has a custom form, the fields attribute will be populated with user’s answers.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 400 if the repo is not gated.
HfHubHTTPError — HTTP 403 if you only have read-only access to the repo. This can be the case if you don’t have write or admin role in the organization the repo belongs to or if you passed a read token.

Get pending access requests for a given gated repo.

A pending request means the user has requested access to the repo but the request has not been processed yet. If the approval mode is automatic, this list should be empty. Pending requests can be accepted or rejected using accept_access_request() and reject_access_request().

For more info about gated repos, see https://huggingface.co/docs/hub/models-gated.

Example:

Copied
from huggingface_hub import list_pending_access_requests, accept_access_request

# List pending requests
requests = list(list_pending_access_requests("meta-llama/Llama-2-7b"))
len(requests)
411
requests[0]
[
    AccessRequest(
        username='clem',
        fullname='Clem 🤗',
        email='***',
        timestamp=datetime.datetime(2023, 11, 23, 18, 4, 53, 828000, tzinfo=datetime.timezone.utc),
        status='pending',
        fields=None,
    ),
    ...
]

# Accept Clem's request
accept_access_request("meta-llama/Llama-2-7b", "clem")
list_rejected_access_requests
<
source
>
( repo_id: strrepo_type: str | None = Nonetoken: bool | str | None = None ) → Iterable[AccessRequest]

Expand 3 parameters
Parameters

repo_id (str) — The id of the repo to get access requests for.
repo_type (str, optional) — The type of the repo to get access requests for. Must be one of model, dataset or space. Defaults to model.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[AccessRequest]

An iterable of AccessRequest objects. Each time contains a username, email, status and timestamp attribute. If the gated repo has a custom form, the fields attribute will be populated with user’s answers.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 400 if the repo is not gated.
HfHubHTTPError — HTTP 403 if you only have read-only access to the repo. This can be the case if you don’t have write or admin role in the organization the repo belongs to or if you passed a read token.

Get rejected access requests for a given gated repo.

A rejected request means the user has requested access to the repo and the request has been explicitly rejected by a repo owner (either you or another user from your organization). The user cannot download any file of the repo. Rejected requests can be accepted or cancelled at any time using accept_access_request() and cancel_access_request(). A cancelled request will go back to the pending list while an accepted request will go to the accepted list.

For more info about gated repos, see https://huggingface.co/docs/hub/models-gated.

Example:

Copied
from huggingface_hub import list_rejected_access_requests

requests = list(list_rejected_access_requests("meta-llama/Llama-2-7b"))
len(requests)
411
requests[0]
[
    AccessRequest(
        username='clem',
        fullname='Clem 🤗',
        email='***',
        timestamp=datetime.datetime(2023, 11, 23, 18, 4, 53, 828000, tzinfo=datetime.timezone.utc),
        status='rejected',
        fields=None,
    ),
    ...
]
list_repo_commits
<
source
>
( repo_id: strrepo_type: str | None = Nonetoken: bool | str | None = Nonerevision: str | None = Noneformatted: bool = False ) → list[GitCommitInfo]

Expand 5 parameters
Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
repo_type (str, optional) — Set to "dataset" or "space" if listing commits from a dataset or a Space, None or "model" if listing from a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
revision (str, optional) — The git revision to commit from. Defaults to the head of the "main" branch.
formatted (bool) — Whether to return the HTML-formatted title and description of the commits. Defaults to False.
Returns

list[GitCommitInfo]

list of objects containing information about the commits for a repo on the Hub.


Raises

RepositoryNotFoundError or RevisionNotFoundError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.
RevisionNotFoundError — If revision is not found (error 404) on the repo.

Get the list of commits of a given revision for a repo on the Hub.

Commits are sorted by date (last commit first).

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()

# Commits are sorted by date (last commit first)
initial_commit = api.list_repo_commits("gpt2")[-1]

# Initial commit is always a system commit containing the `.gitattributes` file.
initial_commit
GitCommitInfo(
    commit_id='9b865efde13a30c13e0a33e536cf3e4a5a9d71d8',
    authors=['system'],
    created_at=datetime.datetime(2019, 2, 18, 10, 36, 15, tzinfo=datetime.timezone.utc),
    title='initial commit',
    message='',
    formatted_title=None,
    formatted_message=None
)

# Create an empty branch by deriving from initial commit
api.create_branch("gpt2", "new_empty_branch", revision=initial_commit.commit_id)
list_repo_files
<
source
>
( repo_id: strrevision: str | None = Nonerepo_type: str | None = Nonetoken: str | bool | None = None ) → list[str]

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
revision (str, optional) — The revision of the repository from which to get the information.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

list[str]

the list of files in a given repository.


Get the list of files in a given repo.

list_repo_likers
<
source
>
( repo_id: strrepo_type: str | None = Nonetoken: bool | str | None = None ) → Iterable[User]

Parameters

repo_id (str) — The repository to retrieve . Example: "user/my-cool-model".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
Returns

Iterable[User]

an iterable of huggingface_hub.hf_api.User objects.


List all users who liked a given repo on the hugging Face Hub.

See also list_liked_repos().

list_repo_refs
<
source
>
( repo_id: strrepo_type: str | None = Noneinclude_pull_requests: bool = Falsetoken: str | bool | None = None ) → GitRefs

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
repo_type (str, optional) — Set to "dataset", "space" or "kernel" if listing refs from a dataset, a Space or a Kernel, None or "model" if listing from a model. Default is None.
include_pull_requests (bool, optional) — Whether to include refs from pull requests in the list. Defaults to False.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

GitRefs

object containing all information about branches and tags for a repo on the Hub.


Get the list of refs of a given repo (both tags and branches).

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
api.list_repo_refs("gpt2")
GitRefs(branches=[GitRefInfo(name='main', ref='refs/heads/main', target_commit='e7da7f221d5bf496a48136c0cd264e630fe9fcc8')], converts=[], tags=[])

api.list_repo_refs("bigcode/the-stack", repo_type='dataset')
GitRefs(
    branches=[
        GitRefInfo(name='main', ref='refs/heads/main', target_commit='18edc1591d9ce72aa82f56c4431b3c969b210ae3'),
        GitRefInfo(name='v1.1.a1', ref='refs/heads/v1.1.a1', target_commit='f9826b862d1567f3822d3d25649b0d6d22ace714')
    ],
    converts=[],
    tags=[
        GitRefInfo(name='v1.0', ref='refs/tags/v1.0', target_commit='c37a8cd1e382064d8aced5e05543c5f7753834da')
    ]
)
list_repo_tree
<
source
>
( repo_id: strpath_in_repo: str | None = Nonerecursive: bool = Falseexpand: bool = Falserevision: str | None = Nonerepo_type: str | None = Nonetoken: str | bool | None = None ) → Iterable[Union[RepoFile, RepoFolder]]

Expand 7 parameters
Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
path_in_repo (str, optional) — Relative path of the tree (folder) in the repo, for example: "checkpoints/1fec34a/results". Will default to the root tree (folder) of the repository.
recursive (bool, optional, defaults to False) — Whether to list tree’s files and folders recursively.
expand (bool, optional, defaults to False) — Whether to fetch more information about the tree’s files and folders (e.g. last commit and files’ security scan results). This operation is more expensive for the server so only 50 results are returned per page (instead of 1000). As pagination is implemented in huggingface_hub, this is transparent for you except for the time it takes to get the results.
revision (str, optional) — The revision of the repository from which to get the tree. Defaults to "main" branch.
repo_type (str, optional) — The type of the repository from which to get the tree ("model", "dataset", "space" or "kernel"). Defaults to "model".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[Union[RepoFile, RepoFolder]]

The information about the tree’s files and folders, as an iterable of RepoFile and RepoFolder objects. The order of the files and folders is not guaranteed.


Raises

RepositoryNotFoundError or RevisionNotFoundError or ~utils.RemoteEntryNotFoundError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.
RevisionNotFoundError — If revision is not found (error 404) on the repo.
~utils.RemoteEntryNotFoundError — If the tree (folder) does not exist (error 404) on the repo.

List a repo tree’s files and folders and get information about them.

Examples:

Get information about a repo’s tree.

Copied
from huggingface_hub import list_repo_tree
repo_tree = list_repo_tree("lysandre/arxiv-nlp")
repo_tree
<generator object HfApi.list_repo_tree at 0x7fa4088e1ac0>
list(repo_tree)
[
    RepoFile(path='.gitattributes', size=391, blob_id='ae8c63daedbd4206d7d40126955d4e6ab1c80f8f', lfs=None, last_commit=None, security=None),
    RepoFile(path='README.md', size=391, blob_id='43bd404b159de6fba7c2f4d3264347668d43af25', lfs=None, last_commit=None, security=None),
    RepoFile(path='config.json', size=554, blob_id='2f9618c3a19b9a61add74f70bfb121335aeef666', lfs=None, last_commit=None, security=None),
    RepoFile(
        path='flax_model.msgpack', size=497764107, blob_id='8095a62ccb4d806da7666fcda07467e2d150218e',
        lfs={'size': 497764107, 'sha256': 'd88b0d6a6ff9c3f8151f9d3228f57092aaea997f09af009eefd7373a77b5abb9', 'pointer_size': 134}, last_commit=None, security=None
    ),
    RepoFile(path='merges.txt', size=456318, blob_id='226b0752cac7789c48f0cb3ec53eda48b7be36cc', lfs=None, last_commit=None, security=None),
    RepoFile(
        path='pytorch_model.bin', size=548123560, blob_id='64eaa9c526867e404b68f2c5d66fd78e27026523',
        lfs={'size': 548123560, 'sha256': '9be78edb5b928eba33aa88f431551348f7466ba9f5ef3daf1d552398722a5436', 'pointer_size': 134}, last_commit=None, security=None
    ),
    RepoFile(path='vocab.json', size=898669, blob_id='b00361fece0387ca34b4b8b8539ed830d644dbeb', lfs=None, last_commit=None, security=None)]
]
Get even more information about a repo’s tree (last commit and files’ security scan results)

Copied
from huggingface_hub import list_repo_tree
repo_tree = list_repo_tree("prompthero/openjourney-v4", expand=True)
list(repo_tree)
[
    RepoFolder(
        path='feature_extractor',
        tree_id='aa536c4ea18073388b5b0bc791057a7296a00398',
        last_commit={
            'oid': '47b62b20b20e06b9de610e840282b7e6c3d51190',
            'title': 'Upload diffusers weights (#48)',
            'date': datetime.datetime(2023, 3, 21, 9, 5, 27, tzinfo=datetime.timezone.utc)
        }
    ),
    RepoFolder(
        path='safety_checker',
        tree_id='65aef9d787e5557373fdf714d6c34d4fcdd70440',
        last_commit={
            'oid': '47b62b20b20e06b9de610e840282b7e6c3d51190',
            'title': 'Upload diffusers weights (#48)',
            'date': datetime.datetime(2023, 3, 21, 9, 5, 27, tzinfo=datetime.timezone.utc)
        }
    ),
    RepoFile(
        path='model_index.json',
        size=582,
        blob_id='d3d7c1e8c3e78eeb1640b8e2041ee256e24c9ee1',
        lfs=None,
        last_commit={
            'oid': 'b195ed2d503f3eb29637050a886d77bd81d35f0e',
            'title': 'Fix deprecation warning by changing `CLIPFeatureExtractor` to `CLIPImageProcessor`. (#54)',
            'date': datetime.datetime(2023, 5, 15, 21, 41, 59, tzinfo=datetime.timezone.utc)
        },
        security={
            'safe': True,
            'av_scan': {'virusFound': False, 'virusNames': None},
            'pickle_import_scan': None
        }
    )
    ...
]
list_scheduled_jobs
<
source
>
( timeout: int | None = Nonenamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

timeout (float, optional) — Whether to set a timeout for the request to the Hub.
namespace (str, optional) — The namespace from where it lists the jobs. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
List scheduled compute Jobs on Hugging Face infrastructure.

list_spaces
<
source
>
( filter: str | Iterable[str] | None = Noneauthor: str | None = Nonesearch: str | None = Nonedatasets: str | Iterable[str] | None = Nonemodels: str | Iterable[str] | None = Nonelinked: bool = Falsesort: SpaceSort_T | None = Nonelimit: int | None = Noneexpand: list[ExpandSpaceProperty_T] | None = Nonefull: bool | None = Nonetoken: bool | str | None = None ) → Iterable[SpaceInfo]

Expand 11 parameters
Parameters

filter (str or Iterable, optional) — A string tag or list of tags that can be used to identify Spaces on the Hub.
author (str, optional) — A string which identify the author of the returned Spaces.
search (str, optional) — A string that will be contained in the returned Spaces.
datasets (str or Iterable, optional) — Whether to return Spaces that make use of a dataset. The name of a specific dataset can be passed as a string.
models (str or Iterable, optional) — Whether to return Spaces that make use of a model. The name of a specific model can be passed as a string.
linked (bool, optional) — Whether to return Spaces that make use of either a model or a dataset.
sort (SpaceSort_T, optional) — The key with which to sort the resulting spaces. Possible values are “created_at”, “last_modified”, “likes” and “trending_score”.
limit (int, optional) — The limit on the number of Spaces fetched. Leaving this option to None fetches all Spaces.
expand (list[ExpandSpaceProperty_T], optional) — List properties to return in the response. When used, only the properties in the list will be returned. This parameter cannot be used if full is passed. Possible values are "author", "cardData", "datasets", "disabled", "lastModified", "createdAt", "likes", "models", "private", "runtime", "sdk", "siblings", "sha", "subdomain", "tags", "trendingScore", "usedStorage", and "resourceGroup".
full (bool, optional) — Whether to fetch all Spaces data, including the last_modified, siblings and card_data fields.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[SpaceInfo]

an iterable of huggingface_hub.hf_api.SpaceInfo objects.


List spaces hosted on the Huggingface Hub, given some filters.

list_spaces_hardware
<
source
>
( token: bool | str | None = None ) → list[JobHardwareInfo]

Returns

list[JobHardwareInfo]

A list of available hardware configurations.


List available hardware options for Spaces.

Example:

Copied
from huggingface_hub import list_spaces_hardware
hardware_list = list_spaces_hardware()
hardware_list[0]
JobHardwareInfo(name='cpu-basic', pretty_name='CPU Basic', cpu='2 vCPU', ram='16 GB', ...)
hardware_list[0].name
'cpu-basic'
list_user_followers
<
source
>
( username: strtoken: bool | str | None = None ) → Iterable[User]

Parameters

username (str) — Username of the user to get the followers of.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[User]

A list of User objects with the followers of the user.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 404 If the user does not exist on the Hub.

Get the list of followers of a user on the Hub.

list_user_following
<
source
>
( username: strtoken: bool | str | None = None ) → Iterable[User]

Parameters

username (str) — Username of the user to get the users followed by.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[User]

A list of User objects with the users followed by the user.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 404 If the user does not exist on the Hub.

Get the list of users followed by a user on the Hub.

list_user_repos
<
source
>
( namespace: str | None = Nonetoken: bool | str | None = None ) → Iterable[RepoStorageInfo]

Parameters

namespace (str, optional) — Organization name. If not provided, lists repos for the authenticated user.
token (bool or str, optional) — A valid user access token. Defaults to the locally saved token.
Returns

Iterable[RepoStorageInfo]

An iterable of RepoStorageInfo objects.


List all repositories (models, datasets, spaces, buckets) for a user or organization with storage info.

Uses the /api/settings/repositories endpoint for the authenticated user or /api/organizations/{namespace}/settings/repositories for an organization.

Example:

Copied
from huggingface_hub import list_user_repos

repos = list(list_user_repos())
repos[0]
RepoStorageInfo(id='username/my-model', type='model', ...)

# List repos from an organization
repos = list(list_user_repos(namespace="my-org"))
list_webhooks
<
source
>
( token: bool | str | None = None ) → list[WebhookInfo]

Parameters

token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

list[WebhookInfo]

List of webhook info objects.


List all configured webhooks.

Example:

Copied
from huggingface_hub import list_webhooks
webhooks = list_webhooks()
len(webhooks)
2
webhooks[0]
WebhookInfo(
    id="654bbbc16f2ec14d77f109cc",
    watched=[WebhookWatchedItem(type="user", name="julien-c"), WebhookWatchedItem(type="org", name="HuggingFaceH4")],
    url="https://webhook.site/a2176e82-5720-43ee-9e06-f91cb4c91548",
    secret="my-secret",
    domains=["repo", "discussion"],
    disabled=False,
)
merge_pull_request
<
source
>
( repo_id: strdiscussion_num: inttoken: bool | str | None = Nonecomment: str | None = Nonerepo_type: str | None = None ) → DiscussionStatusChange

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
discussion_num (int) — The number of the Discussion or Pull Request . Must be a strictly positive integer.
comment (str, optional) — An optional comment to post with the status change.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

DiscussionStatusChange

the status change event


Merges a Pull Request.

Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
model_info
<
source
>
( repo_id: strrevision: str | None = Nonetimeout: float | None = NonesecurityStatus: bool | None = Nonefiles_metadata: bool = Falseexpand: list[ExpandModelProperty_T] | None = Nonetoken: bool | str | None = None ) → huggingface_hub.hf_api.ModelInfo

Expand 7 parameters
Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
revision (str, optional) — The revision of the model repository from which to get the information.
timeout (float, optional) — Whether to set a timeout for the request to the Hub.
securityStatus (bool, optional) — Whether to retrieve the security status from the model repository as well. The security status will be returned in the security_repo_status field.
files_metadata (bool, optional) — Whether or not to retrieve metadata for files in the repository (size, LFS metadata, etc). Defaults to False.
expand (list[ExpandModelProperty_T], optional) — List properties to return in the response. When used, only the properties in the list will be returned. This parameter cannot be used if securityStatus or files_metadata are passed. Possible values are "author", "baseModels", "cardData", "childrenModelCount", "config", "createdAt", "disabled", "downloads", "downloadsAllTime", "evalResults", "gated", "gguf", "inference", "inferenceProviderMapping", "lastModified", "library_name", "likes", "mask_token", "model-index", "pipeline_tag", "private", "safetensors", "sha", "siblings", "spaces", "tags", "transformersInfo", "trendingScore", "widgetData", "usedStorage", and "resourceGroup".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

huggingface_hub.hf_api.ModelInfo

The model repository information.


Get info on one specific model on huggingface.co

Model can be private if you pass an acceptable token or are logged in.

Raises the following errors:

RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
RevisionNotFoundError If the revision to download from cannot be found.
move_bucket
<
source
>
( from_id: strto_id: strtoken: bool | str | None = None )

Parameters

from_id (str) — A namespace (user or an organization) and a bucket name separated by a /. Original bucket identifier (e.g. "username/my-bucket").
to_id (str) — A namespace (user or an organization) and a bucket name separated by a /. Final bucket identifier (e.g. "username/new-bucket-name" or "organization/my-bucket").
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

BucketNotFoundError

BucketNotFoundError — If the source bucket cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.

Move a bucket from “namespace1/repo_name1” to “namespace2/repo_name2”

Note there are certain limitations. For more information about moving repositories, please see https://hf.co/docs/hub/repositories-settings#renaming-or-transferring-a-repo.

Example:

Copied
from huggingface_hub import move_bucket

# Rename a bucket within the same namespace
move_bucket(from_id="username/old-name", to_id="username/new-name")

# Transfer a bucket to an organization
move_bucket(from_id="username/my-bucket", to_id="my-org/my-bucket")
move_repo
<
source
>
( from_id: strto_id: strrepo_type: str | None = Nonetoken: str | bool | None = None )

Parameters

from_id (str) — A namespace (user or an organization) and a repo name separated by a /. Original repository identifier.
to_id (str) — A namespace (user or an organization) and a repo name separated by a /. Final repository identifier.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Moving a repository from namespace1/repo_name1 to namespace2/repo_name2

Note there are certain limitations. For more information about moving repositories, please see https://hf.co/docs/hub/repositories-settings#renaming-or-transferring-a-repo.

Raises the following errors:

RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
paper_info
<
source
>
( id: str ) → PaperInfo

Parameters

id (str, optional) — ArXiv id of the paper.
Returns

PaperInfo

A PaperInfo object.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 404 If the paper does not exist on the Hub.

Get information for a paper on the Hub.

parse_safetensors_file_metadata
<
source
>
( repo_id: strfilename: strrepo_type: str | None = Nonerevision: str | None = Nonetoken: bool | str | None = None ) → SafetensorsFileMetadata

Expand 5 parameters
Parameters

repo_id (str) — A user or an organization name and a repo name separated by a /.
filename (str) — The name of the file in the repo.
repo_type (str, optional) — Set to "dataset" or "space" if the file is in a dataset or space, None or "model" if in a model. Default is None.
revision (str, optional) — The git revision to fetch the file from. Can be a branch name, a tag, or a commit hash. Defaults to the head of the "main" branch.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SafetensorsFileMetadata

information related to a safetensors file.


Raises

NotASafetensorsRepoError or SafetensorsParsingError

NotASafetensorsRepoError — If the repo is not a safetensors repo i.e. doesn’t have either a model.safetensors or a model.safetensors.index.json file.
SafetensorsParsingError — If a safetensors file header couldn’t be parsed correctly.

Parse metadata from a safetensors file on the Hub.

To parse metadata from all safetensors files in a repo at once, use get_safetensors_metadata().

For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

pause_inference_endpoint
<
source
>
( name: strnamespace: str | None = Nonetoken: bool | str | None = None ) → InferenceEndpoint

Parameters

name (str) — The name of the Inference Endpoint to pause.
namespace (str, optional) — The namespace in which the Inference Endpoint is located. Defaults to the current user.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

InferenceEndpoint

information about the paused Inference Endpoint.


Pause an Inference Endpoint.

A paused Inference Endpoint will not be charged. It can be resumed at any time using resume_inference_endpoint(). This is different than scaling the Inference Endpoint to zero with scale_to_zero_inference_endpoint(), which would be automatically restarted when a request is made to it.

For convenience, you can also pause an Inference Endpoint using pause_inference_endpoint().

pause_space
<
source
>
( repo_id: strtoken: bool | str | None = None ) → SpaceRuntime

Expand 2 parameters
Parameters

repo_id (str) — ID of the Space to pause. Example: "Salesforce/BLIP2".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SpaceRuntime

Runtime information about your Space including stage=PAUSED and requested hardware.


Raises

RepositoryNotFoundError or HfHubHTTPError or BadRequestError

RepositoryNotFoundError — If your Space is not found (error 404). Most probably wrong repo_id or your space is private but you are not authenticated.
HfHubHTTPError — 403 Forbidden: only the owner of a Space can pause it. If you want to manage a Space that you don’t own, either ask the owner by opening a Discussion or duplicate the Space.
BadRequestError — If your Space is a static Space. Static Spaces are always running and never billed. If you want to hide a static Space, you can set it to private.

Pause your Space.

A paused Space stops executing until manually restarted by its owner. This is different from the sleeping state in which free Spaces go after 48h of inactivity. Paused time is not billed to your account, no matter the hardware you’ve selected. To restart your Space, use restart_space() and go to your Space settings page.

For more details, please visit the docs.

permanently_delete_lfs_files
<
source
>
( repo_id: strlfs_files: Iterable[LFSFileInfo]rewrite_history: bool = Truerepo_type: str | None = Nonetoken: bool | str | None = None )

Parameters

repo_id (str) — The repository for which you are listing LFS files.
lfs_files (Iterable[LFSFileInfo]) — An iterable of LFSFileInfo items to permanently delete from the repo. Use list_lfs_files() to list all LFS files from a repo.
rewrite_history (bool, optional, default to True) — Whether to rewrite repository history to remove file pointers referencing the deleted LFS files (recommended).
repo_type (str, optional) — Type of repository. Set to "dataset" or "space" if listing from a dataset or space, None or "model" if listing from a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Permanently delete LFS files from a repo on the Hub.

This is a permanent action that will affect all commits referencing the deleted files and might corrupt your repository. This is a non-revertible operation. Use it only if you know what you are doing.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
lfs_files = api.list_lfs_files("username/my-cool-repo")

# Filter files files to delete based on a combination of `filename`, `pushed_at`, `ref` or `size`.
# e.g. select only LFS files in the "checkpoints" folder
lfs_files_to_delete = (lfs_file for lfs_file in lfs_files if lfs_file.filename.startswith("checkpoints/"))

# Permanently delete LFS files
api.permanently_delete_lfs_files("username/my-cool-repo", lfs_files_to_delete)
preupload_lfs_files
<
source
>
( repo_id: stradditions: Iterable[CommitOperationAdd]token: str | bool | None = Nonerepo_type: str | None = Nonerevision: str | None = Nonecreate_pr: bool | None = Nonenum_threads: int = 5free_memory: bool = Truegitignore_content: str | None = None )

Expand 9 parameters
Parameters

repo_id (str) — The repository in which you will commit the files, for example: "username/custom_transformers".
additions (Iterable of CommitOperationAdd) — The list of files to upload. Warning: the objects in this list will be mutated to include information relative to the upload. Do not reuse the same objects for multiple commits.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — The type of repository to upload to (e.g. "model" -default-, "dataset" or "space").
revision (str, optional) — The git revision to commit from. Defaults to the head of the "main" branch.
create_pr (boolean, optional) — Whether or not you plan to create a Pull Request with that commit. Defaults to False.
num_threads (int, optional) — Number of concurrent threads for uploading files. Defaults to 5. Setting it to 2 means at most 2 files will be uploaded concurrently.
free_memory (bool, optional, defaults to True) — If True, the path_or_fileobj attribute of each CommitOperationAdd is replaced by an empty bytes object after upload to save memory. Set to False if you need to reuse the operation objects outside of a subsequent create_commit() call.
gitignore_content (str, optional) — The content of the .gitignore file to know which files should be ignored. The order of priority is to first check if gitignore_content is passed, then check if the .gitignore file is present in the list of files to commit and finally default to the .gitignore file already hosted on the Hub (if any).
Pre-upload LFS files to S3 in preparation on a future commit.

This method is useful if you are generating the files to upload on-the-fly and you don’t want to store them in memory before uploading them all at once.

This is a power-user method. You shouldn’t need to call it directly to make a normal commit. Use create_commit() directly instead.

Commit operations will be mutated during the process. In particular, the attached path_or_fileobj will be removed after the upload to save memory (and replaced by an empty bytes object). Do not reuse the same objects except to pass them to create_commit(). If you don’t want to remove the attached content from the commit operation object, pass free_memory=False.

Example:

Copied
from huggingface_hub import CommitOperationAdd, preupload_lfs_files, create_commit, create_repo

repo_id = create_repo("test_preupload").repo_id

# Generate and preupload LFS files one by one
operations = [] # List of all `CommitOperationAdd` objects that will be generated
for i in range(5):
    content = ... # generate binary content
    addition = CommitOperationAdd(path_in_repo=f"shard_{i}_of_5.bin", path_or_fileobj=content)
    preupload_lfs_files(repo_id, additions=[addition]) # upload + free memory
    operations.append(addition)

# Create commit
create_commit(repo_id, operations=operations, commit_message="Commit all shards")
read_paper
<
source
>
( id: str ) → str

Parameters

id (str) — ArXiv id of the paper.
Returns

str

The paper page content as markdown.


Raises

HfHubHTTPError

HfHubHTTPError — HTTP 404 If the paper does not exist on the Hub.

Get the markdown content of a paper page on the Hub.

reject_access_request
<
source
>
( repo_id: struser: strrepo_type: str | None = Nonerejection_reason: str | Nonetoken: bool | str | None = None )

Expand 5 parameters
Parameters

repo_id (str) — The id of the repo to reject access request for.
user (str) — The username of the user which access request should be rejected.
repo_type (str, optional) — The type of the repo to reject access request for. Must be one of model, dataset or space. Defaults to model.
rejection_reason (str, optional) — Optional rejection reason that will be visible to the user (max 200 characters).
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

HfHubHTTPError

HfHubHTTPError — HTTP 400 if the repo is not gated.
HfHubHTTPError — HTTP 403 if you only have read-only access to the repo. This can be the case if you don’t have write or admin role in the organization the repo belongs to or if you passed a read token.
HfHubHTTPError — HTTP 404 if the user does not exist on the Hub.
HfHubHTTPError — HTTP 404 if the user access request cannot be found.
HfHubHTTPError — HTTP 404 if the user access request is already in the rejected list.

Reject an access request from a user for a given gated repo.

A rejected request will go to the rejected list. The user cannot download any file of the repo. Rejected requests can be accepted or cancelled at any time using accept_access_request() and cancel_access_request(). A cancelled request will go back to the pending list while an accepted request will go to the accepted list.

For more info about gated repos, see https://huggingface.co/docs/hub/models-gated.

rename_discussion
<
source
>
( repo_id: strdiscussion_num: intnew_title: strtoken: bool | str | None = Nonerepo_type: str | None = None ) → DiscussionTitleChange

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
discussion_num (int) — The number of the Discussion or Pull Request . Must be a strictly positive integer.
new_title (str) — The new title for the discussion
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

DiscussionTitleChange

the title change event


Renames a Discussion.

Examples:

Copied
new_title = "New title, fixing a typo"
HfApi().rename_discussion(
    repo_id="username/repo_name",
    discussion_num=34
    new_title=new_title
)
# DiscussionTitleChange(id='deadbeef0000000', type='title-change', ...)
Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
repo_exists
<
source
>
( repo_id: strrepo_type: str | None = Nonetoken: str | bool | None = None )

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
repo_type (str, optional) — Set to "dataset" or "space" if getting repository info from a dataset or a space, None or "model" if getting repository info from a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Checks if a repository exists on the Hugging Face Hub.

Examples:

Copied
from huggingface_hub import repo_exists
repo_exists("google/gemma-7b")
True
repo_exists("google/not-a-repo")
False
repo_info
<
source
>
( repo_id: strrevision: str | None = Nonerepo_type: str | None = Nonetimeout: float | None = Nonefiles_metadata: bool = Falseexpand: ExpandModelProperty_T | ExpandDatasetProperty_T | ExpandSpaceProperty_T | None = Nonetoken: bool | str | None = None ) → Union[SpaceInfo, DatasetInfo, ModelInfo]

Expand 7 parameters
Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
revision (str, optional) — The revision of the repository from which to get the information.
repo_type (str, optional) — Set to "dataset" or "space" if getting repository info from a dataset or a space, None or "model" if getting repository info from a model. Default is None.
timeout (float, optional) — Whether to set a timeout for the request to the Hub.
expand (ExpandModelProperty_T or ExpandDatasetProperty_T or ExpandSpaceProperty_T, optional) — List properties to return in the response. When used, only the properties in the list will be returned. This parameter cannot be used if files_metadata is passed. For an exhaustive list of available properties, check out model_info(), dataset_info() or space_info().
files_metadata (bool, optional) — Whether or not to retrieve metadata for files in the repository (size, LFS metadata, etc). Defaults to False.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Union[SpaceInfo, DatasetInfo, ModelInfo]

The repository information, as a huggingface_hub.hf_api.DatasetInfo, huggingface_hub.hf_api.ModelInfo or huggingface_hub.hf_api.SpaceInfo object.


Get the info object for a given repo of a given type.

Raises the following errors:

RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
RevisionNotFoundError If the revision to download from cannot be found.
request_space_hardware
<
source
>
( repo_id: strhardware: SpaceHardwaretoken: bool | str | None = Nonesleep_time: int | None = None ) → SpaceRuntime

Parameters

repo_id (str) — ID of the repo to update. Example: "bigcode/in-the-stack".
hardware (str or SpaceHardware) — Hardware on which to run the Space. Example: "t4-medium".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
sleep_time (int, optional) — Number of seconds of inactivity to wait before a Space is put to sleep. Set to -1 if you don’t want your Space to sleep (default behavior for upgraded hardware). For free hardware, you can’t configure the sleep time (value is fixed to 48 hours of inactivity). See https://huggingface.co/docs/hub/spaces-gpus#sleep-time for more details.
Returns

SpaceRuntime

Runtime information about a Space including Space stage and hardware.


Request new hardware for a Space.

It is also possible to request hardware directly when creating the Space repo! See create_repo() for details.

request_space_storage
<
source
>
( repo_id: strstorage: SpaceStoragetoken: bool | str | None = None ) → SpaceRuntime

Parameters

repo_id (str) — ID of the Space to update. Example: "open-llm-leaderboard/open_llm_leaderboard".
storage (str or SpaceStorage) — Storage tier. Either ‘small’, ‘medium’, or ‘large’.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SpaceRuntime

Runtime information about a Space including Space stage and hardware.


Request persistent storage for a Space.

request_space_storage is deprecated and will be removed in version 2.0. Use set_space_volumes() instead.

restart_space
<
source
>
( repo_id: strtoken: bool | str | None = Nonefactory_reboot: bool = False ) → SpaceRuntime

Expand 3 parameters
Parameters

repo_id (str) — ID of the Space to restart. Example: "Salesforce/BLIP2".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
factory_reboot (bool, optional) — If True, the Space will be rebuilt from scratch without caching any requirements.
Returns

SpaceRuntime

Runtime information about your Space.


Raises

RepositoryNotFoundError or HfHubHTTPError or BadRequestError

RepositoryNotFoundError — If your Space is not found (error 404). Most probably wrong repo_id or your space is private but you are not authenticated.
HfHubHTTPError — 403 Forbidden: only the owner of a Space can restart it. If you want to restart a Space that you don’t own, either ask the owner by opening a Discussion or duplicate the Space.
BadRequestError — If your Space is a static Space. Static Spaces are always running and never billed. If you want to hide a static Space, you can set it to private.

Restart your Space.

This is the only way to programmatically restart a Space if you’ve put it on Pause (see pause_space()). You must be the owner of the Space to restart it. If you are using an upgraded hardware, your account will be billed as soon as the Space is restarted. You can trigger a restart no matter the current state of a Space.

For more details, please visit the docs.

resume_inference_endpoint
<
source
>
( name: strnamespace: str | None = Nonerunning_ok: bool = Truetoken: bool | str | None = None ) → InferenceEndpoint

Parameters

name (str) — The name of the Inference Endpoint to resume.
namespace (str, optional) — The namespace in which the Inference Endpoint is located. Defaults to the current user.
running_ok (bool, optional) — If True, the method will not raise an error if the Inference Endpoint is already running. Defaults to True.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

InferenceEndpoint

information about the resumed Inference Endpoint.


Resume an Inference Endpoint.

For convenience, you can also resume an Inference Endpoint using InferenceEndpoint.resume().

resume_scheduled_job
<
source
>
( scheduled_job_id: strnamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

scheduled_job_id (str) — ID of the scheduled Job.
namespace (str, optional) — The namespace where the scheduled Job is. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Resume (unpause) a scheduled compute Job on Hugging Face infrastructure.

revision_exists
<
source
>
( repo_id: strrevision: strrepo_type: str | None = Nonetoken: str | bool | None = None )

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
revision (str) — The revision of the repository to check.
repo_type (str, optional) — Set to "dataset" or "space" if getting repository info from a dataset or a space, None or "model" if getting repository info from a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Checks if a specific revision exists on a repo on the Hugging Face Hub.

Examples:

Copied
from huggingface_hub import revision_exists
revision_exists("google/gemma-7b", "float16")
True
revision_exists("google/gemma-7b", "not-a-revision")
False
run_as_future
<
source
>
( fn: Callable[..., R]*args**kwargs ) → Future

Parameters

fn (Callable) — The method to run in the background.
*args, **kwargs — Arguments with which the method will be called.
Returns

Future

a Future instance to get the result of the task.


Run a method in the background and return a Future instance.

The main goal is to run methods without blocking the main thread (e.g. to push data during a training). Background jobs are queued to preserve order but are not ran in parallel. If you need to speed-up your scripts by parallelizing lots of call to the API, you must setup and use your own ThreadPoolExecutor.

Note: Most-used methods like upload_file(), upload_folder() and create_commit() have a run_as_future: bool argument to directly call them in the background. This is equivalent to calling api.run_as_future(...) on them but less verbose.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
future = api.run_as_future(api.whoami) # instant
future.done()
False
future.result() # wait until complete and return result
(...)
future.done()
True
run_job
<
source
>
( image: strcommand: list[str]env: dict[str, Any] | None = Nonesecrets: dict[str, Any] | None = Noneflavor: JobHardware | str | None = Nonetimeout: int | float | str | None = Nonelabels: dict[str, str] | None = Nonevolumes: list[Volume] | None = Noneexpose: list[int] | None = Nonessh: bool = Falsenamespace: str | None = Nonetoken: bool | str | None = None )

Expand 12 parameters
Parameters

image (str) — The Docker image to use. Examples: "ubuntu", "python:3.12", "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel". Example with an image from a Space: "hf.co/spaces/lhoestq/duckdb".
command (list[str]) — The command to run. Example: ["echo", "hello"].
env (dict[str, Any], optional) — Defines the environment variables for the Job.
secrets (dict[str, Any], optional) — Defines the secret environment variables for the Job.
flavor (str, optional) — Flavor for the hardware. See JobHardware for possible values. Defaults to "cpu-basic".
timeout (Union[int, float, str], optional) — Max duration for the Job: int/float with s (seconds, default), m (minutes), h (hours) or d (days). Example: 300 or "5m" for 5 minutes.
labels (dict[str, str], optional) — Labels to attach to the job (key-value pairs).
volumes (list[Volume], optional) — Hugging Face Buckets or Repos to mount as volumes in the job container. Each volume is a Volume with type ("bucket", "model", "dataset", or "space"), source (e.g. "username/my-bucket"), and mount_path (e.g. "/data").
expose (list[int], optional) — Container ports to expose through the jobs proxy. Each listed port is reachable on the public jobs domain (e.g. https://<job_id>--8000.hf.jobs). Access always requires an HF token with read access to the job’s namespace.
ssh (bool, optional) — If True, the job’s container is reachable over SSH at the URL given by job.status.ssh_url (e.g. ssh <job_id>@ssh.hf.jobs, or hf jobs ssh <job_id> from the CLI). Connecting requires write access to the job’s namespace and an SSH public key registered on the Hub (https://huggingface.co/settings/keys). Defaults to False.
namespace (str, optional) — The namespace where the Job will be created. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Run compute Jobs on Hugging Face infrastructure.

Example:

Run your first Job:

Copied
from huggingface_hub import run_job
run_job(image="python:3.12", command=["python", "-c" ,"print('Hello from HF compute!')"])
Run a GPU Job:

Copied
from huggingface_hub import run_job
image = "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel"
command = ["python", "-c", "import torch; print(f"This code ran with the following GPU: {torch.cuda.get_device_name()}")"]
run_job(image=image, command=command, flavor="a10g-small")
Run a Job with volumes:

Copied
from huggingface_hub import Volume, run_job
dataset_volume = Volume(type="dataset", source="HuggingFaceFW/fineweb", mount_path="/data")
output_bucket_volume = Volume(type="bucket", source="username/my-bucket", mount_path="/output")
image = "duckdb/duckdb"
command = ["duckdb", "-c", "COPY (SELECT * FROM '/data/**/*.parquet' LIMIT 5) TO '/output/first-rows.parquet'"]
run_job(image=image, command=command, volumes=[dataset_volume, output_bucket_volume])
run_uv_job
<
source
>
( script: strscript_args: list[str] | None = Nonedependencies: list[str] | None = Nonepython: str | None = Noneimage: str | None = Noneenv: dict[str, Any] | None = Nonesecrets: dict[str, Any] | None = Noneflavor: JobHardware | str | None = Nonetimeout: int | float | str | None = Nonelabels: dict[str, str] | None = Nonevolumes: list[Volume] | None = Noneexpose: list[int] | None = Nonessh: bool = Falsenamespace: str | None = Nonetoken: bool | str | None = None )

Expand 15 parameters
Parameters

script (str) — Path or URL of the UV script, or a command.
script_args (list[str], optional) — Arguments to pass to the script or command.
dependencies (list[str], optional) — Dependencies to use to run the UV script.
python (str, optional) — Use a specific Python version. Default is 3.12.
image (str, optional, defaults to “ghcr.io/astral-sh/uv —python3.12-bookworm”): Use a custom Docker image with uv installed.
env (dict[str, Any], optional) — Defines the environment variables for the Job.
secrets (dict[str, Any], optional) — Defines the secret environment variables for the Job.
flavor (str, optional) — Flavor for the hardware. See JobHardware for possible values. Defaults to "cpu-basic".
timeout (Union[int, float, str], optional) — Max duration for the Job: int/float with s (seconds, default), m (minutes), h (hours) or d (days). Example: 300 or "5m" for 5 minutes.
labels (dict[str, str], optional) — Labels to attach to the job (key-value pairs).
volumes (list[Volume], optional) — Hugging Face Buckets or Repos to mount as volumes in the job container. Each volume is a Volume with type ("bucket", "model", "dataset", or "space"), source (e.g. "username/my-bucket"), and mount_path (e.g. "/data").
expose (list[int], optional) — Container ports to expose through the jobs proxy. Each listed port is reachable on the public jobs domain (e.g. https://<job_id>--8000.hf.jobs). Access always requires an HF token with read access to the job’s namespace.
ssh (bool, optional) — If True, the job’s container is reachable over SSH at the URL given by job.status.ssh_url (e.g. ssh <job_id>@ssh.hf.jobs, or hf jobs ssh <job_id> from the CLI). Connecting requires write access to the job’s namespace and an SSH public key registered on the Hub (https://huggingface.co/settings/keys). Defaults to False.
namespace (str, optional) — The namespace where the Job will be created. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Run a UV script Job on Hugging Face infrastructure.

Example:

Run a script from a URL:

Copied
from huggingface_hub import run_uv_job
script = "https://raw.githubusercontent.com/huggingface/trl/refs/heads/main/trl/scripts/sft.py"
script_args = ["--model_name_or_path", "Qwen/Qwen2-0.5B", "--dataset_name", "trl-lib/Capybara", "--push_to_hub"]
run_uv_job(script, script_args=script_args, dependencies=["trl"], flavor="a10g-small")
Run a local script:

Copied
from huggingface_hub import run_uv_job
script = "my_sft.py"
script_args = ["--model_name_or_path", "Qwen/Qwen2-0.5B", "--dataset_name", "trl-lib/Capybara", "--push_to_hub"]
run_uv_job(script, script_args=script_args, dependencies=["trl"], flavor="a10g-small")
Run a command:

Copied
from huggingface_hub import run_uv_job
script = "lighteval"
script_args= ["endpoint", "inference-providers", "model_name=openai/gpt-oss-20b,provider=auto", "lighteval|gsm8k|0|0"]
run_uv_job(script, script_args=script_args, dependencies=["lighteval"], flavor="a10g-small")
Mount volumes, e.g. to save model checkpoints during training:

Copied
from huggingface_hub import Volume, run_uv_job
script = "my_sft.py"
script_args = ["--output_dir", "/training-outputs/training-v3-final", ...]
checkpoints_bucket = Volume(type="bucket", source="username/my-bucket", mount_path="/training-outputs")
run_uv_job(script, script_args=script_args, volumes=[checkpoints_bucket])
scale_to_zero_inference_endpoint
<
source
>
( name: strnamespace: str | None = Nonetoken: bool | str | None = None ) → InferenceEndpoint

Parameters

name (str) — The name of the Inference Endpoint to scale to zero.
namespace (str, optional) — The namespace in which the Inference Endpoint is located. Defaults to the current user.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

InferenceEndpoint

information about the scaled-to-zero Inference Endpoint.


Scale Inference Endpoint to zero.

An Inference Endpoint scaled to zero will not be charged. It will be resume on the next request to it, with a cold start delay. This is different than pausing the Inference Endpoint with pause_inference_endpoint(), which would require a manual resume with resume_inference_endpoint().

For convenience, you can also scale an Inference Endpoint to zero using InferenceEndpoint.scale_to_zero().

search_spaces
<
source
>
( query: strfilter: str | Iterable[str] | None = Nonesdk: str | list[str] | None = Noneinclude_non_running: bool = Falsetoken: bool | str | None = None ) → Iterable[SpaceSearchResult]

Parameters

query (str) — The search query string.
filter (str or Iterable[str], optional) — A string tag or list of tags to filter by.
sdk (str or list[str], optional) — Filter by SDK (e.g. "gradio", "docker", "static").
include_non_running (bool, optional) — Whether to include non-running Spaces in results. Defaults to False.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

Iterable[SpaceSearchResult]

an iterable of SpaceSearchResult objects.


Search Spaces on the Hub using semantic search.

This endpoint uses semantic search (embedding-based) for multi-word queries and full-text search for single-word queries.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
results = list(api.search_spaces("generate image"))
results[0].id
'mrfakename/Z-Image-Turbo'
results[0].ai_category
'Image Generation'
set_space_sleep_time
<
source
>
( repo_id: strsleep_time: inttoken: bool | str | None = None ) → SpaceRuntime

Parameters

repo_id (str) — ID of the repo to update. Example: "bigcode/in-the-stack".
sleep_time (int, optional) — Number of seconds of inactivity to wait before a Space is put to sleep. Set to -1 if you don’t want your Space to pause (default behavior for upgraded hardware). For free hardware, you can’t configure the sleep time (value is fixed to 48 hours of inactivity). See https://huggingface.co/docs/hub/spaces-gpus#sleep-time for more details.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SpaceRuntime

Runtime information about a Space including Space stage and hardware.


Set a custom sleep time for a Space running on upgraded hardware..

Your Space will go to sleep after X seconds of inactivity. You are not billed when your Space is in “sleep” mode. If a new visitor lands on your Space, it will “wake it up”. Only upgraded hardware can have a configurable sleep time. To know more about the sleep stage, please refer to https://huggingface.co/docs/hub/spaces-gpus#sleep-time.

It is also possible to set a custom sleep time when requesting hardware with request_space_hardware().

set_space_volumes
<
source
>
( repo_id: strvolumes: list[Volume]token: bool | str | None = None )

Parameters

repo_id (str) — ID of the Space to update. Example: "username/my-space".
volumes (list[Volume]) — List of Volume objects to mount. Each volume has a type ("bucket", "model", "dataset", or "space"), a source (repo or bucket ID), a mount_path (path inside the container), and optional revision, read_only, and path fields.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

BadRequestError

BadRequestError — If the Space is a static Space (volumes are not supported on static Spaces).

Set volumes for a Space.

Sets (or replaces) the list of volumes mounted in the Space. Each volume gives the Space’s container access to a Hub resource (model, dataset, or storage bucket).

Example:

Copied
from huggingface_hub import HfApi, Volume
api = HfApi()
api.set_space_volumes(
    "username/my-space",
    volumes=[
        Volume(type="model", source="username/my-model", mount_path="/models", read_only=True),
        Volume(type="bucket", source="username/my-bucket", mount_path="/data"),
    ],
)
snapshot_download
<
source
>
( repo_id: strrepo_type: str | None = Nonerevision: str | None = Nonecache_dir: str | Path | None = Nonelocal_dir: str | Path | None = Noneetag_timeout: float = 10force_download: bool = Falsetoken: bool | str | None = Nonelocal_files_only: bool = Falseallow_patterns: list[str] | str | None = Noneignore_patterns: list[str] | str | None = Nonemax_workers: int = 8tqdm_class: type[base_tqdm] | None = Nonedry_run: bool = False ) → str or list of DryRunFileInfo

Expand 14 parameters
Parameters

repo_id (str) — A user or an organization name and a repo name separated by a /.
repo_type (str, optional) — Set to "dataset" or "space" if downloading from a dataset or space, None or "model" if downloading from a model. Default is None.
revision (str, optional) — An optional Git revision id which can be a branch name, a tag, or a commit hash.
cache_dir (str, Path, optional) — Path to the folder where cached files are stored.
local_dir (str or Path, optional) — If provided, the downloaded files will be placed under this directory.
etag_timeout (float, optional, defaults to 10) — When fetching ETag, how many seconds to wait for the server to send data before giving up which is passed to httpx.request.
force_download (bool, optional, defaults to False) — Whether the file should be downloaded even if it already exists in the local cache.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
local_files_only (bool, optional, defaults to False) — If True, avoid downloading the file and return the path to the local cached file if it exists.
allow_patterns (list[str] or str, optional) — If provided, only files matching at least one pattern are downloaded.
ignore_patterns (list[str] or str, optional) — If provided, files matching any of the patterns are not downloaded.
max_workers (int, optional) — Number of concurrent threads to download files (1 thread = 1 file download). Defaults to 8.
tqdm_class (tqdm, optional) — If provided, overwrites the default behavior for the progress bar. Passed argument must inherit from tqdm.auto.tqdm or at least mimic its behavior. Note that the tqdm_class is not passed to each individual download. Defaults to the custom HF progress bar that can be disabled by setting HF_HUB_DISABLE_PROGRESS_BARS environment variable.
dry_run (bool, optional, defaults to False) — If True, perform a dry run without actually downloading the files. Returns a list of DryRunFileInfo objects containing information about what would be downloaded.
Returns

str or list of DryRunFileInfo

If dry_run=False: Folder path of the repo snapshot.
If dry_run=True: A list of DryRunFileInfo objects containing download information.

Raises

RepositoryNotFoundError or RevisionNotFoundError or EnvironmentError or OSError or ValueError

RepositoryNotFoundError — If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
RevisionNotFoundError — If the revision to download from cannot be found.
EnvironmentError — If token=True and the token cannot be found.
OSError — if ETag cannot be determined.
ValueError — if some parameter value is invalid.

Download repo files.

Download a whole snapshot of a repo’s files at the specified revision. This is useful when you want all files from a repo, because you don’t know which ones you will need a priori. All files are nested inside a folder in order to keep their actual filename relative to that folder. You can also filter which files to download using allow_patterns and ignore_patterns.

If local_dir is provided, the file structure from the repo will be replicated in this location. When using this option, the cache_dir will not be used and a .cache/huggingface/ folder will be created at the root of local_dir to store some metadata related to the downloaded files.While this mechanism is not as robust as the main cache-system, it’s optimized for regularly pulling the latest version of a repository.

An alternative would be to clone the repo but this requires git and git-lfs to be installed and properly configured. It is also not possible to filter which files to download when cloning a repository using git.

space_info
<
source
>
( repo_id: strrevision: str | None = Nonetimeout: float | None = Nonefiles_metadata: bool = Falseexpand: list[ExpandSpaceProperty_T] | None = Nonetoken: bool | str | None = None ) → SpaceInfo

Expand 6 parameters
Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
revision (str, optional) — The revision of the space repository from which to get the information.
timeout (float, optional) — Whether to set a timeout for the request to the Hub.
files_metadata (bool, optional) — Whether or not to retrieve metadata for files in the repository (size, LFS metadata, etc). Defaults to False.
expand (list[ExpandSpaceProperty_T], optional) — List properties to return in the response. When used, only the properties in the list will be returned. This parameter cannot be used if full is passed. Possible values are "author", "cardData", "createdAt", "datasets", "disabled", "lastModified", "likes", "models", "private", "runtime", "sdk", "siblings", "sha", "subdomain", "tags", "trendingScore", "usedStorage", and "resourceGroup".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

SpaceInfo

The space repository information.


Get info on one specific Space on huggingface.co.

Space can be private if you pass an acceptable token.

Raises the following errors:

RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
RevisionNotFoundError If the revision to download from cannot be found.
super_squash_history
<
source
>
( repo_id: strbranch: str | None = Nonecommit_message: str | None = Nonerepo_type: str | None = Nonetoken: str | bool | None = None )

Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
branch (str, optional) — The branch to squash. Defaults to the head of the "main" branch.
commit_message (str, optional) — The commit message to use for the squashed commit.
repo_type (str, optional) — Set to "dataset" or "space" if listing commits from a dataset or a Space, None or "model" if listing from a model. Default is None.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Raises

RepositoryNotFoundError or RevisionNotFoundError or BadRequestError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.
RevisionNotFoundError — If the branch to squash cannot be found.
BadRequestError — If invalid reference for a branch. You cannot squash history on tags.

Squash commit history on a branch for a repo on the Hub.

Squashing the repo history is useful when you know you’ll make hundreds of commits and you don’t want to clutter the history. Squashing commits can only be performed from the head of a branch.

Once squashed, the commit history cannot be retrieved. This is a non-revertible operation.

Once the history of a branch has been squashed, it is not possible to merge it back into another branch since their history will have diverged.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()

# Create repo
repo_id = api.create_repo("test-squash").repo_id

# Make a lot of commits.
api.upload_file(repo_id=repo_id, path_in_repo="file.txt", path_or_fileobj=b"content")
api.upload_file(repo_id=repo_id, path_in_repo="lfs.bin", path_or_fileobj=b"content")
api.upload_file(repo_id=repo_id, path_in_repo="file.txt", path_or_fileobj=b"another_content")

# Squash history
api.super_squash_history(repo_id=repo_id)
suspend_scheduled_job
<
source
>
( scheduled_job_id: strnamespace: str | None = Nonetoken: bool | str | None = None )

Parameters

scheduled_job_id (str) — ID of the scheduled Job.
namespace (str, optional) — The namespace where the scheduled Job is. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Suspend (pause) a scheduled compute Job on Hugging Face infrastructure.

sync_bucket
<
source
>
( source: str | None = Nonedest: str | None = Nonedelete: bool = Falseignore_times: bool = Falseignore_sizes: bool = Falseexisting: bool = Falseignore_existing: bool = Falseinclude: list[str] | None = Noneexclude: list[str] | None = Nonefilter_from: str | None = Noneplan: str | None = Noneapply: str | None = Nonedry_run: bool = Falseverbose: bool = Falsequiet: bool = Falsetoken: bool | str | None = None ) → [SyncPlan]

Expand 16 parameters
Parameters

source (str, optional) — Source path: local directory or hf://buckets/namespace/bucket_name(/prefix). Required unless using apply.
dest (str, optional) — Destination path: local directory or hf://buckets/namespace/bucket_name(/prefix). Required unless using apply.
delete (bool, optional, defaults to False) — Delete destination files not present in source.
ignore_times (bool, optional, defaults to False) — Skip files only based on size, ignoring modification times.
ignore_sizes (bool, optional, defaults to False) — Skip files only based on modification times, ignoring sizes.
existing (bool, optional, defaults to False) — Skip creating new files on receiver (only update existing files).
ignore_existing (bool, optional, defaults to False) — Skip updating files that exist on receiver (only create new files).
include (list[str], optional) — Include files matching patterns (fnmatch-style).
exclude (list[str], optional) — Exclude files matching patterns (fnmatch-style).
filter_from (str, optional) — Path to a filter file with include/exclude rules.
plan (str, optional) — Save sync plan to this JSONL file instead of executing.
apply (str, optional) — Apply a previously saved plan file. When set, source and dest are not needed.
dry_run (bool, optional, defaults to False) — Print sync plan to stdout as JSONL without executing.
verbose (bool, optional, defaults to False) — Show detailed per-file operations.
quiet (bool, optional, defaults to False) — Suppress all output and progress bars.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used.
Returns

[SyncPlan]

The computed (or loaded) sync plan.


Sync files between a local directory and a bucket.

This is equivalent to the hf buckets sync CLI command. One of source or dest must be a bucket path (hf://buckets/...) and the other must be a local directory path.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()

# Upload local directory to bucket
api.sync_bucket("./data", "hf://buckets/username/my-bucket")

# Download bucket to local directory
api.sync_bucket("hf://buckets/username/my-bucket", "./data")

# Sync with delete and filtering
api.sync_bucket(
    "./data",
    "hf://buckets/username/my-bucket",
    delete=True,
    include=["*.safetensors"],
)

# Dry run: preview what would be synced
plan = api.sync_bucket("./data", "hf://buckets/username/my-bucket", dry_run=True)
plan.summary()
{'uploads': 3, 'downloads': 0, 'deletes': 0, 'skips': 1, 'total_size': 4096}

# Save plan for review, then apply
api.sync_bucket("./data", "hf://buckets/username/my-bucket", plan="sync-plan.jsonl")
api.sync_bucket(apply="sync-plan.jsonl")
unlike
<
source
>
( repo_id: strtoken: bool | str | None = Nonerepo_type: str | None = None )

Parameters

repo_id (str) — The repository to unlike. Example: "user/my-cool-model".
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if unliking a dataset or space, None or "model" if unliking a model. Default is None.
Raises

RepositoryNotFoundError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.

Unlike a given repo on the Hub (e.g. remove from favorite list).

To prevent spam usage, it is not possible to like a repository from a script.

See also list_liked_repos().

Example:

Copied
from huggingface_hub import list_liked_repos, unlike
"gpt2" in list_liked_repos().models # we assume you have already liked gpt2
True
unlike("gpt2")
"gpt2" in list_liked_repos().models
False
update_collection_item
<
source
>
( collection_slug: stritem_object_id: strnote: str | None = Noneposition: int | None = Nonetoken: bool | str | None = None )

Parameters

collection_slug (str) — Slug of the collection to update. Example: "TheBloke/recent-models-64f9a55bb3115b4f513ec026".
item_object_id (str) — ID of the item in the collection. This is not the id of the item on the Hub (repo_id or paper id). It must be retrieved from a CollectionItem object. Example: collection.items[0].item_object_id.
note (str, optional) — A note to attach to the item in the collection. The maximum size for a note is 500 characters.
position (int, optional) — New position of the item in the collection.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Update an item in a collection.

Example:

Copied
from huggingface_hub import get_collection, update_collection_item

# Get collection first
collection = get_collection("TheBloke/recent-models-64f9a55bb3115b4f513ec026")

# Update item based on its ID (add note + update position)
update_collection_item(
    collection_slug="TheBloke/recent-models-64f9a55bb3115b4f513ec026",
    item_object_id=collection.items[-1].item_object_id,
    note="Newly updated model!"
    position=0,
)
update_collection_metadata
<
source
>
( collection_slug: strtitle: str | None = Nonedescription: str | None = Noneposition: int | None = Noneprivate: bool | None = Nonetheme: str | None = Nonetoken: bool | str | None = None )

Parameters

collection_slug (str) — Slug of the collection to update. Example: "TheBloke/recent-models-64f9a55bb3115b4f513ec026".
title (str) — Title of the collection to update.
description (str, optional) — Description of the collection to update.
position (int, optional) — New position of the collection in the list of collections of the user.
private (bool, optional) — Whether the collection should be private or not.
theme (str, optional) — Theme of the collection on the Hub.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Update metadata of a collection on the Hub.

All arguments are optional. Only provided metadata will be updated.

Returns: Collection

Example:

Copied
from huggingface_hub import update_collection_metadata
collection = update_collection_metadata(
    collection_slug="username/iccv-2023-64f9a55bb3115b4f513ec026",
    title="ICCV Oct. 2023"
    description="Portfolio of models, datasets, papers and demos I presented at ICCV Oct. 2023",
    private=False,
    theme="pink",
)
collection.slug
"username/iccv-oct-2023-64f9a55bb3115b4f513ec026"
# ^collection slug got updated but not the trailing ID
update_inference_endpoint
<
source
>
( name: straccelerator: str | None = Noneinstance_size: str | None = Noneinstance_type: str | None = Nonemin_replica: int | None = Nonemax_replica: int | None = Nonescale_to_zero_timeout: int | None = Nonescaling_metric: InferenceEndpointScalingMetric | None = Nonescaling_threshold: float | None = Nonerepository: str | None = Noneframework: str | None = Nonerevision: str | None = Nonetask: str | None = Nonecustom_image: dict | None = Noneenv: dict[str, str] | None = Nonesecrets: dict[str, str] | None = Nonedomain: str | None = Nonepath: str | None = Nonecache_http_responses: bool | None = Nonetags: list[str] | None = Nonenamespace: str | None = Nonetoken: bool | str | None = None ) → InferenceEndpoint

Expand 22 parameters
Parameters

name (str) — The name of the Inference Endpoint to update.
accelerator (str, optional) — The hardware accelerator to be used for inference (e.g. "cpu").
instance_size (str, optional) — The size or type of the instance to be used for hosting the model (e.g. "x4").
instance_type (str, optional) — The cloud instance type where the Inference Endpoint will be deployed (e.g. "intel-icl").
min_replica (int, optional) — The minimum number of replicas (instances) to keep running for the Inference Endpoint.
max_replica (int, optional) — The maximum number of replicas (instances) to scale to for the Inference Endpoint.
scale_to_zero_timeout (int, optional) — The duration in minutes before an inactive endpoint is scaled to zero.
scaling_metric (str or InferenceEndpointScalingMetric , optional) — The metric reference for scaling. Either “pendingRequests” or “hardwareUsage” when provided. Defaults to None.
scaling_threshold (float, optional) — The scaling metric threshold used to trigger a scale up. Ignored when scaling metric is not provided. Defaults to None.
repository (str, optional) — The name of the model repository associated with the Inference Endpoint (e.g. "gpt2").
framework (str, optional) — The machine learning framework used for the model (e.g. "custom").
revision (str, optional) — The specific model revision to deploy on the Inference Endpoint (e.g. "6c0e6080953db56375760c0471a8c5f2929baf11").
task (str, optional) — The task on which to deploy the model (e.g. "text-classification").
custom_image (dict, optional) — A custom Docker image to use for the Inference Endpoint. This is useful if you want to deploy an Inference Endpoint running on the text-generation-inference (TGI) framework (see examples).
env (dict[str, str], optional) — Non-secret environment variables to inject in the container environment
secrets (dict[str, str], optional) — Secret values to inject in the container environment.
domain (str, optional) — The custom domain for the Inference Endpoint deployment, if setup the inference endpoint will be available at this domain (e.g. "my-new-domain.cool-website.woof").
path (str, optional) — The custom path to the deployed model, should start with a / (e.g. "/models/google-bert/bert-base-uncased").
cache_http_responses (bool, optional) — Whether to cache HTTP responses from the Inference Endpoint.
tags (list[str], optional) — A list of tags to associate with the Inference Endpoint.
namespace (str, optional) — The namespace where the Inference Endpoint will be updated. Defaults to the current user’s namespace.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

InferenceEndpoint

information about the updated Inference Endpoint.


Update an Inference Endpoint.

This method allows the update of either the compute configuration, the deployed model, the route, or any combination. All arguments are optional but at least one must be provided.

For convenience, you can also update an Inference Endpoint using InferenceEndpoint.update().

update_job_labels
<
source
>
( job_id: strlabels: dict[str, str]namespace: str | None = Nonetoken: bool | str | None = None ) → JobInfo

Parameters

job_id (str) — ID of the Job.
labels (dict[str, str]) — New labels to set on the job. Replaces all existing labels. Both keys and values must be max 100 characters and contain only alphanumeric characters, dots, dashes, and underscores.
namespace (str, optional) — The namespace where the Job is running. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Returns

JobInfo

The updated Job info.


Update labels of an existing Job.

Replaces all existing user-provided labels with the new labels.

update_repo_settings
<
source
>
( repo_id: strgated: Literal['auto', 'manual', False] | None = Noneprivate: bool | None = Nonevisibility: RepoVisibility_T | None = Nonetoken: str | bool | None = Nonerepo_type: str | None = None )

Expand 6 parameters
Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
gated (Literal["auto", "manual", False], optional) — The gated status for the repository. If set to None (default), the gated setting of the repository won’t be updated.
“auto”: The repository is gated, and access requests are automatically approved or denied based on predefined criteria.
“manual”: The repository is gated, and access requests require manual approval.
False : The repository is not gated, and anyone can access it.
private (bool, optional) — Whether the repository should be private. Cannot be passed together with visibility.
visibility (Literal["public", "private", "protected"], optional) — Visibility of the repository. Can be "public" or "private", or "protected" for Spaces.
token (Union[str, bool, None], optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — The type of the repository to update settings from ("model", "dataset" or "space"). Defaults to "model".
Raises

ValueError or HfHubHTTPError or RepositoryNotFoundError

ValueError — If gated is not one of “auto”, “manual”, or False.
ValueError — If repo_type is not one of the values in constants.REPO_TYPES.
HfHubHTTPError — If the request to the Hugging Face Hub API fails.
RepositoryNotFoundError — If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.

Update the settings of a repository, including gated access and visibility.

To give more control over how repos are used, the Hub allows repo authors to enable access requests for their repos, and also to change the visibility of the repo.

update_scheduled_job_labels
<
source
>
( scheduled_job_id: strlabels: dict[str, str]namespace: str | None = Nonetoken: bool | str | None = None ) → ScheduledJobInfo

Parameters

scheduled_job_id (str) — ID of the scheduled Job.
labels (dict[str, str]) — New labels to set on the scheduled job. Replaces all existing labels. Both keys and values must be max 100 characters and contain only alphanumeric characters, dots, dashes, and underscores.
namespace (str, optional) — The namespace where the scheduled Job is. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Returns

ScheduledJobInfo

The updated scheduled Job info.


Update labels of an existing scheduled Job.

Replaces all existing user-provided labels with the new labels.

update_webhook
<
source
>
( webhook_id: strurl: str | None = Nonewatched: list[dict | WebhookWatchedItem] | None = Nonedomains: list[constants.WEBHOOK_DOMAIN_T] | None = Nonesecret: str | None = Nonetoken: bool | str | None = None ) → WebhookInfo

Parameters

webhook_id (str) — The unique identifier of the webhook to be updated.
url (str, optional) — The URL to which the payload will be sent.
watched (list[WebhookWatchedItem], optional) — List of items to watch. It can be users, orgs, models, datasets, or spaces. Refer to WebhookWatchedItem for more details. Watched items can also be provided as plain dictionaries.
domains (list[Literal["repo", "discussion"]], optional) — The domains to watch. This can include “repo”, “discussion”, or both.
secret (str, optional) — A secret to sign the payload with, providing an additional layer of security.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

WebhookInfo

Info about the updated webhook.


Update an existing webhook.

Example:

Copied
from huggingface_hub import update_webhook
updated_payload = update_webhook(
    webhook_id="654bbbc16f2ec14d77f109cc",
    url="https://new.webhook.site/a2176e82-5720-43ee-9e06-f91cb4c91548",
    watched=[{"type": "user", "name": "julien-c"}, {"type": "org", "name": "HuggingFaceH4"}],
    domains=["repo"],
    secret="my-secret",
)
print(updated_payload)
WebhookInfo(
    id="654bbbc16f2ec14d77f109cc",
    job=None,
    url="https://new.webhook.site/a2176e82-5720-43ee-9e06-f91cb4c91548",
    watched=[WebhookWatchedItem(type="user", name="julien-c"), WebhookWatchedItem(type="org", name="HuggingFaceH4")],
    domains=["repo"],
    secret="my-secret",
    disabled=False,
upload_file
<
source
>
( path_or_fileobj: str | Path | bytes | BinaryIOpath_in_repo: strrepo_id: strtoken: str | bool | None = Nonerepo_type: str | None = Nonerevision: str | None = Nonecommit_message: str | None = Nonecommit_description: str | None = Nonecreate_pr: bool | None = Noneparent_commit: str | None = Nonerun_as_future: bool = False_hot_reload: bool | None = None ) → CommitInfo or Future

Expand 11 parameters
Parameters

path_or_fileobj (str, Path, bytes, or IO) — Path to a file on the local machine or binary data stream / fileobj / buffer.
path_in_repo (str) — Relative filepath in the repo, for example: "checkpoints/1fec34a/weights.bin"
repo_id (str) — The repository to which the file will be uploaded, for example: "username/custom_transformers"
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
revision (str, optional) — The git revision to commit from. Defaults to the head of the "main" branch.
commit_message (str, optional) — The summary / title / first line of the generated commit
commit_description (str optional) — The description of the generated commit
create_pr (boolean, optional) — Whether or not to create a Pull Request with that commit. Defaults to False. If revision is not set, PR is opened against the "main" branch. If revision is set and is a branch, PR is opened against this branch. If revision is set and is not a branch name (example: a commit oid), an RevisionNotFoundError is returned by the server.
parent_commit (str, optional) — The OID / SHA of the parent commit, as a hexadecimal string. Shorthands (7 first characters) are also supported. If specified and create_pr is False, the commit will fail if revision does not point to parent_commit. If specified and create_pr is True, the pull request will be created from parent_commit. Specifying parent_commit ensures the repo has not changed before committing the changes, and can be especially useful if the repo is updated / committed to concurrently.
run_as_future (bool, optional) — Whether or not to run this method in the background. Background jobs are run sequentially without blocking the main thread. Passing run_as_future=True will return a Future object. Defaults to False.
Returns

CommitInfo or Future

Instance of CommitInfo containing information about the newly created commit (commit hash, commit url, pr url, commit message,…). If run_as_future=True is passed, returns a Future object which will contain the result when executed.


Upload a local file (up to 50 GB) to the given repo. The upload is done through a HTTP post request, and doesn’t require git or git-lfs to be installed.

Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
RepositoryNotFoundError If the repository to download from cannot be found. This may be because it doesn’t exist, or because it is set to private and you do not have access.
RevisionNotFoundError If the revision to download from cannot be found.
upload_file assumes that the repo already exists on the Hub. If you get a Client error 404, please make sure you are authenticated, that your token has the required permissions, and that repo_id and repo_type are set correctly. If repo does not exist, create it first using create_repo().

Example:

Copied
from huggingface_hub import upload_file

with open("./local/filepath", "rb") as fobj:
    upload_file(
        path_or_fileobj=fileobj,
        path_in_repo="remote/file/path.h5",
        repo_id="username/my-dataset",
        repo_type="dataset",
        token="my_token",
    )

upload_file(
    path_or_fileobj=".\\local\\file\\path",
    path_in_repo="remote/file/path.h5",
    repo_id="username/my-model",
    token="my_token",
)

upload_file(
    path_or_fileobj=".\\local\\file\\path",
    path_in_repo="remote/file/path.h5",
    repo_id="username/my-model",
    token="my_token",
    create_pr=True,
)
upload_folder
<
source
>
( repo_id: strfolder_path: str | Pathpath_in_repo: str | None = Nonecommit_message: str | None = Nonecommit_description: str | None = Nonetoken: str | bool | None = Nonerepo_type: str | None = Nonerevision: str | None = Nonecreate_pr: bool | None = Noneparent_commit: str | None = Noneallow_patterns: list[str] | str | None = Noneignore_patterns: list[str] | str | None = Nonedelete_patterns: list[str] | str | None = Nonerun_as_future: bool = False ) → CommitInfo or Future

Expand 14 parameters
Parameters

repo_id (str) — The repository to which the file will be uploaded, for example: "username/custom_transformers"
folder_path (str or Path) — Path to the folder to upload on the local file system
path_in_repo (str, optional) — Relative path of the directory in the repo, for example: "checkpoints/1fec34a/results". Will default to the root folder of the repository.
token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
repo_type (str, optional) — Set to "dataset" or "space" if uploading to a dataset or space, None or "model" if uploading to a model. Default is None.
revision (str, optional) — The git revision to commit from. Defaults to the head of the "main" branch.
commit_message (str, optional) — The summary / title / first line of the generated commit. Defaults to: f"Upload {path_in_repo} with huggingface_hub"
commit_description (str optional) — The description of the generated commit
create_pr (boolean, optional) — Whether or not to create a Pull Request with that commit. Defaults to False. The PR is always opened against the default branch: setting both create_pr=True and revision raises a ValueError. Note that each call with create_pr=True opens a new pull request: to resume an interrupted upload into the existing PR, re-run with revision="refs/pr/N" instead.
parent_commit (str, optional) — The OID / SHA of the parent commit, as a hexadecimal string. Shorthands (7 first characters) are also supported. If specified and create_pr is False, the commit will fail if revision does not point to parent_commit. Specifying parent_commit ensures the repo has not changed before committing the changes, and can be especially useful if the repo is updated / committed to concurrently. If the upload is split into several commits (large folders), parent_commit only applies to the first one.
allow_patterns (list[str] or str, optional) — If provided, only files matching at least one pattern are uploaded.
ignore_patterns (list[str] or str, optional) — If provided, files matching any of the patterns are not uploaded.
delete_patterns (list[str] or str, optional) — If provided, remote files matching any of the patterns will be deleted from the repo while committing new files. This is useful if you don’t know which files have already been uploaded. Note: to avoid discrepancies the .gitattributes file is not deleted even if it matches the pattern.
run_as_future (bool, optional) — Whether or not to run this method in the background. Background jobs are run sequentially without blocking the main thread. Passing run_as_future=True will return a Future object. Defaults to False.
Returns

CommitInfo or Future

Instance of CommitInfo containing information about the newly created commit (commit hash, commit url, pr url, commit message,…). If run_as_future=True is passed, returns a Future object which will contain the result when executed.


Upload a local folder to the given repo. The upload is done through a HTTP requests, and doesn’t require git or git-lfs to be installed.

The structure of the folder will be preserved. Files with the same name already present in the repository will be overwritten. Others will be left untouched.

Use the allow_patterns and ignore_patterns arguments to specify which files to upload. These parameters accept either a single pattern or a list of patterns. Patterns are Standard Wildcards (globbing patterns) as documented here. If both allow_patterns and ignore_patterns are provided, both constraints apply. By default, all files from the folder are uploaded.

Use the delete_patterns argument to specify remote files you want to delete. Input type is the same as for allow_patterns (see above). If path_in_repo is also provided, the patterns are matched against paths relative to this folder. For example, upload_folder(..., path_in_repo="experiment", delete_patterns="logs/*") will delete any remote file under ./experiment/logs/. Note that the .gitattributes file will not be deleted even if it matches the patterns.

Any .git/ folder present in any subdirectory will be ignored. However, please be aware that the .gitignore file is not taken into account.

When hf_xet is installed (the default), files are uploaded through a streamed pipeline: uploads start while the folder is still being checked against the Hub, files are hashed while being chunked for upload (single read pass), and large folders are automatically committed in several batches to stay below server limits (follow-up commits get a (part N) suffix on the commit message). If the upload is interrupted, re-running the same call resumes it: already-committed files are skipped and already-uploaded data is deduplicated. When hf_xet is not installed, falls back to a single commit created with create_commit().

Raises the following errors:

HTTPError if the HuggingFace API returned an error
ValueError if some parameter value is invalid
upload_folder assumes that the repo already exists on the Hub. If you get a Client error 404, please make sure you are authenticated, that your token has the required permissions, and that repo_id and repo_type are set correctly. If repo does not exist, create it first using create_repo().

Example:

Copied
# Upload checkpoints folder except the log files
upload_folder(
    folder_path="local/checkpoints",
    path_in_repo="remote/experiment/checkpoints",
    repo_id="username/my-dataset",
    repo_type="datasets",
    token="my_token",
    ignore_patterns="**/logs/*.txt",
)

# Upload checkpoints folder including logs while deleting existing logs from the repo
# Useful if you don't know exactly which log files have already being pushed
upload_folder(
    folder_path="local/checkpoints",
    path_in_repo="remote/experiment/checkpoints",
    repo_id="username/my-dataset",
    repo_type="datasets",
    token="my_token",
    delete_patterns="**/logs/*.txt",
)

# Upload checkpoints folder while creating a PR
upload_folder(
    folder_path="local/checkpoints",
    path_in_repo="remote/experiment/checkpoints",
    repo_id="username/my-dataset",
    repo_type="datasets",
    token="my_token",
    create_pr=True,
)
upload_large_folder
<
source
>
( repo_id: strfolder_path: str | Pathrepo_type: strrevision: str | None = Noneprivate: bool | None = Noneallow_patterns: list[str] | str | None = Noneignore_patterns: list[str] | str | None = Nonenum_workers: int | None = Noneprint_report: bool = Trueprint_report_every: int = 60 )

Expand 10 parameters
Parameters

repo_id (str) — The repository to which the file will be uploaded. E.g. "HuggingFaceTB/smollm-corpus".
folder_path (str or Path) — Path to the folder to upload on the local file system.
repo_type (str) — Type of the repository. Must be one of "model", "dataset" or "space". Unlike in all other HfApi methods, repo_type is explicitly required here. This is to avoid any mistake when uploading a large folder to the Hub, and therefore prevent from having to re-upload everything.
revision (str, optional) — The branch to commit to. If not provided, the main branch will be used.
private (bool, optional) — Whether the repository should be private. If None (default), the repo will be public unless the organization’s default is private.
allow_patterns (list[str] or str, optional) — If provided, only files matching at least one pattern are uploaded.
ignore_patterns (list[str] or str, optional) — If provided, files matching any of the patterns are not uploaded.
num_workers (int, optional) — Number of workers to start. Defaults to half of CPU cores (minimum 1). A higher number of workers may speed up the process if your machine allows it. However, on machines with a slower connection, it is recommended to keep the number of workers low to ensure better resumability. Indeed, partially uploaded files will have to be completely re-uploaded if the process is interrupted.
print_report (bool, optional) — Whether to print a report of the upload progress. Defaults to True. Report is printed to sys.stdout every X seconds (60 by defaults) and overwrites the previous report.
print_report_every (int, optional) — Frequency at which the report is printed. Defaults to 60 seconds.
Upload a large folder to the Hub in the most resilient way possible.

Several workers are started to upload files in an optimized way. Before being committed to a repo, files must be hashed and be pre-uploaded if they are LFS files. Workers will perform these tasks for each file in the folder. At each step, some metadata information about the upload process is saved in the folder under .cache/.huggingface/ to be able to resume the process if interrupted. The whole process might result in several commits.

A few things to keep in mind:

Repository limits still apply: https://huggingface.co/docs/hub/repositories-recommendations
Do not start several processes in parallel.
You can interrupt and resume the process at any time.
Do not upload the same folder to several repositories. If you need to do so, you must delete the local .cache/.huggingface/ folder first.
While being much more robust to upload large folders, upload_large_folder is more limited than upload_folder() feature-wise. In practice:

you cannot set a custom path_in_repo. If you want to upload to a subfolder, you need to set the proper structure locally.
you cannot set a custom commit_message and commit_description since multiple commits are created.
you cannot delete from the repo while uploading. Please make a separate commit first.
you cannot create a PR directly. Please create a PR first (from the UI or using create_pull_request()) and then commit to it by passing revision.
Technical details:

upload_large_folder process is as follow:

(Check parameters and setup.)
Create repo if missing.
List local files to upload.
Run validation checks and display warnings if repository limits might be exceeded:
Warns if the total number of files exceeds 100k (recommended limit).
Warns if any folder contains more than 10k files (recommended limit).
Warns about files larger than 20GB (recommended) or 50GB (hard limit).
Start workers. Workers can perform the following tasks:
Hash a file.
Get upload mode (regular or LFS) for a list of files.
Pre-upload an LFS file.
Commit a bunch of files. Once a worker finishes a task, it will move on to the next task based on the priority list (see below) until all files are uploaded and committed.
While workers are up, regularly print a report to sys.stdout.
Order of priority:

Commit if more than 5 minutes since last commit attempt (and at least 1 file).
Commit if at least 150 files are ready to commit.
Get upload mode if at least 10 files have been hashed.
Pre-upload LFS file if at least 1 file and no worker is pre-uploading.
Hash file if at least 1 file and no worker is hashing.
Get upload mode if at least 1 file and no worker is getting upload mode.
Pre-upload LFS file if at least 1 file.
Hash file if at least 1 file to hash.
Get upload mode if at least 1 file to get upload mode.
Commit if at least 1 file to commit and at least 1 min since last commit attempt.
Commit if at least 1 file to commit and all other queues are empty.
Special rules:

Only one worker can commit at a time.
If no tasks are available, the worker waits for 10 seconds before checking again.
verify_repo_checksums
<
source
>
( repo_id: strrepo_type: str | None = Nonerevision: str | None = Nonelocal_dir: str | Path | None = Nonecache_dir: str | Path | None = Nonetoken: str | bool | None = None ) → FolderVerification

Expand 6 parameters
Parameters

repo_id (str) — A namespace (user or an organization) and a repo name separated by a /.
repo_type (str, optional) — The type of the repository from which to get the tree ("model", "dataset" or "space". Defaults to "model".
revision (str, optional) — The revision of the repository from which to get the tree. Defaults to "main" branch.
local_dir (str or Path, optional) — The local directory to verify.
cache_dir (str or Path, optional) — The cache directory to verify.
token (Union[bool, str, None], optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
Returns

FolderVerification

a structured result containing the verification details.


Raises

RepositoryNotFoundError or RevisionNotFoundError

RepositoryNotFoundError — If repository is not found (error 404): wrong repo_id/repo_type, private but not authenticated or repo does not exist.
RevisionNotFoundError — If revision is not found (error 404) on the repo.

Verify local files for a repo against Hub checksums.

wait_for_job
<
source
>
( job_id: str | list[str]timeout: float | None = Nonepoll_interval: float = 1.0stages: list[JobStage] | None = Nonenamespace: str | None = Nonetoken: bool | str | None = None ) → JobInfo or list[JobInfo]

Expand 6 parameters
Parameters

job_id (str or list[str]) — ID of the Job, or a list of Job IDs to wait for. If a list is passed, a list of JobInfo is returned (in the same order).
timeout (float, optional) — The maximum time to wait for the Job(s) to finish, in seconds. If None, will wait indefinitely.
poll_interval (float, optional) — The time to wait between each status check, in seconds. Defaults to 1s.
stages (list[JobStage], optional) — The stages to wait for. Defaults to the terminal stages ("COMPLETED", "CANCELED", "ERROR", "DELETED"). Pass e.g. [JobStage.RUNNING] to wait for the Job to start running. Terminal stages always stop the wait regardless of this value.
namespace (str, optional) — The namespace where the Job(s) are running. Defaults to the current user’s namespace.
token (Union[bool, str, None], optional) — A valid user access token. If not provided, the locally saved token will be used, which is the recommended authentication method. Set to False to disable authentication. Refer to: https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Returns

JobInfo or list[JobInfo]

the final Job info(s).


Raises

TimeoutError

TimeoutError — If at least one Job has not reached one of the target stages after timeout seconds.

Wait until one or more compute Jobs on Hugging Face infrastructure reach a given stage.

Each Job status is polled (with inspect_job()) every poll_interval seconds until its stage is one of stages (terminal stages by default: "COMPLETED", "CANCELED", "ERROR" or "DELETED"). The final JobInfo is returned in all cases: a failed or canceled Job does not raise an exception — check job.status.stage to act on the outcome.

Terminal stages always stop the wait, even when not listed in stages. This avoids waiting forever for a stage the Job will never reach (e.g. waiting for "RUNNING" on a Job that fails during scheduling).

Example:

Copied
from huggingface_hub import run_job, wait_for_job
job = run_job(image="python:3.12", command=["python", "-c", "print('Hello from HF compute!')"])
wait_for_job(job_id=job.id).status.stage
'COMPLETED'
wait_for_space
<
source
>
( repo_id: strtimeout: float | None = Nonepoll_interval: float = 1.0token: bool | str | None = None ) → SpaceRuntime

Parameters

repo_id (str) — ID of the Space to wait for. Example: "username/my-space".
timeout (float, optional) — Maximum time to wait in seconds. If None, waits indefinitely.
poll_interval (float, optional) — Seconds between status checks. Defaults to 1s.
token (bool or str, optional) — A valid user access token. Defaults to the locally saved token, which is the recommended authentication method. Set to False to disable authentication. See https://huggingface.co/docs/huggingface_hub/quick-start#authentication.
Returns

SpaceRuntime

The final runtime information once the Space reaches a terminal stage.


Raises

TimeoutError

TimeoutError — If the Space has not reached a terminal stage after timeout seconds.

Wait until a Space reaches a terminal stage (not building/starting).

Polls get_space_runtime() every poll_interval seconds until the Space’s stage is no longer intermediate (BUILDING, RUNNING_BUILDING, APP_STARTING, RUNNING_APP_STARTING). Returns the final SpaceRuntime in all cases — check runtime.stage to act on the outcome (e.g. RUNNING vs BUILD_ERROR).

Example:

Copied
from huggingface_hub import restart_space, wait_for_space
restart_space("username/my-space")
runtime = wait_for_space("username/my-space")
runtime.stage
'RUNNING'
whoami
<
source
>
( token: bool | str | None = Nonecache: bool = False )

Parameters

token (bool or str, optional) — A valid user access token (string). Defaults to the locally saved token, which is the recommended method for authentication (see https://huggingface.co/docs/huggingface_hub/quick-start#authentication). To disable authentication, pass False.
cache (bool, optional) — Whether to cache the result of the whoami call for subsequent calls. If an error occurs during the first call, it won’t be cached. Defaults to False.
Call HF API to know “whoami”.

If passing cache=True, the result will be cached for subsequent calls for the duration of the Python process. This is useful if you plan to call whoami multiple times as this endpoint is heavily rate-limited for security reasons.

API Dataclasses
AccessRequest
class huggingface_hub.hf_api.AccessRequest
<
source
>
( username: strfullname: stremail: str | Nonetimestamp: datetimestatus: Literal['pending', 'accepted', 'rejected']fields: dict[str, Any] | None = None )

Parameters

username (str) — Username of the user who requested access.
fullname (str) — Fullname of the user who requested access.
email (Optional[str]) — Email of the user who requested access. Can only be None in the /accepted list if the user was granted access manually.
timestamp (datetime) — Timestamp of the request.
status (Literal["pending", "accepted", "rejected"]) — Status of the request. Can be one of ["pending", "accepted", "rejected"].
fields (dict[str, Any], optional) — Additional fields filled by the user in the gate form.
Data structure containing information about a user access request.

BucketFile
class huggingface_hub.BucketFile
<
source
>
( **kwargs )

Contains information about a file in a bucket on the Hub. This object is returned by list_bucket_tree().

Similar to RepoFile but for files in buckets.

BucketFileMetadata
class huggingface_hub.BucketFileMetadata
<
source
>
( size: intxet_file_data: XetFileData )

Parameters

size (int) — Size of the file in bytes.
xet_file_data (XetFileData) — Xet information for the file (hash and refresh route).
Data structure containing information about a file in a bucket.

Returned by get_bucket_file_metadata().

BucketInfo
class huggingface_hub.BucketInfo
<
source
>
( **kwargs )

Parameters

id (str) — ID of the bucket.
private (bool) — Is the bucket private.
created_at (datetime) — Date of creation of the bucket on the Hub.
size (int) — Size of the bucket in bytes.
total_files (int) — Total number of files in the bucket.
Contains information about a bucket on the Hub. This object is returned by bucket_info() and list_buckets().

BucketUrl
class huggingface_hub.BucketUrl
<
source
>
( url: strendpoint: str = '' )

Parameters

url (str) — String value of the bucket url.
endpoint (str, optional) — Endpoint of the Hub. Defaults to https://huggingface.co.
Describes a bucket URL on the Hub.

BucketUrl is returned by create_bucket(). At initialization, the URL is parsed to populate properties:

endpoint (str)
namespace (str)
bucket_id (str)
url (str)
uri (HfUri)
DatasetLeaderboardEntry
class huggingface_hub.DatasetLeaderboardEntry
<
source
>
( **kwargs )

Parameters

rank (int) — Rank of the model on the leaderboard (1-indexed).
model_id (str) — ID of the model (e.g. "meta-llama/Llama-3-8b").
value (float) — Evaluation score value.
filename (str) — Name of the result file containing the evaluation data.
verified (bool) — Whether the result has been verified.
source (dict[str, Any]) — Information about the source of the evaluation result. Contains keys like "url", "name", and "isExternal".
author (User or Organization) — The model author, parsed based on the "type" field in the API response.
pull_request (int, optional) — Pull request number associated with the leaderboard entry, if any.
notes (str, optional) — Notes associated with the leaderboard entry, if any.
Contains information about a single entry in a dataset leaderboard on the Hub.

A leaderboard ranks models based on their evaluation scores on a given benchmark dataset. This object is returned by get_dataset_leaderboard(). To get evaluation results for a specific model across benchmarks, see ModelInfo.eval_results (via model_info() with expand=["evalResults"]) and EvalResultEntry.

EvalResultEntry
class huggingface_hub.EvalResultEntry
<
source
>
( dataset_id: strtask_id: strvalue: typing.Anydataset_revision: str | None = Noneverify_token: str | None = Nonedate: str | None = Nonesource_url: str | None = Nonesource_name: str | None = Nonesource_user: str | None = Nonesource_org: str | None = Nonenotes: str | None = None )

Parameters

dataset_id (str) — Benchmark dataset ID from the Hub. Example: “cais/hle”, “Idavidrein/gpqa”.
task_id (str) — Task identifier within the benchmark. Example: “gpqa_diamond”.
value (Any) — The metric value. Example: 20.90.
dataset_revision (str, optional) — Git SHA of the benchmark dataset.
verify_token (str, optional) — A signature that can be used to prove that evaluation is provably auditable and reproducible.
date (str, optional) — When the evaluation was run (ISO-8601 datetime). Defaults to git commit time.
source_url (str, optional) — Link to the evaluation source (e.g., https://huggingface.co/spaces/SaylorTwift/smollm3-mmlu-pro). Required if source_name, source_user, or source_org is provided.
source_name (str, optional) — Display name for the source. Example: “Eval Logs”.
source_user (str, optional) — HF user name for attribution. Example: “celinah”.
source_org (str, optional) — HF org name for attribution. Example: “cais”.
notes (str, optional) — Details about the evaluation setup. Example: “tools”, “no-tools”, “chain-of-thought”.
Evaluation result entry for the .eval_results/*.yaml format.

Represents evaluation scores stored in model repos that automatically appear on the model page and the benchmark dataset’s leaderboard.

For the legacy model-index format in README.md, use EvalResult instead.

See https://huggingface.co/docs/hub/eval-results for more details.

Example:

Copied
from huggingface_hub import EvalResultEntry
# Minimal example with required fields only
result = EvalResultEntry(
    dataset_id="Idavidrein/gpqa",
    task_id="gpqa_diamond",
    value=0.412,
)
# Full example with all fields
result = EvalResultEntry(
    dataset_id="cais/hle",
    task_id="default",
    value=20.90,
    dataset_revision="5503434ddd753f426f4b38109466949a1217c2bb",
    verify_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    date="2025-01-15T10:30:00Z",
    source_url="https://huggingface.co/datasets/cais/hle",
    source_name="CAIS HLE",
    source_org="cais",
    notes="no-tools",
)
SyncOperation
class huggingface_hub.SyncOperation
<
source
>
( action: typing.Literal['upload', 'download', 'delete', 'skip']path: strsize: int | None = Nonereason: str = ''local_mtime: str | None = Noneremote_mtime: str | None = Nonebucket_file: huggingface_hub._buckets.BucketFile | None = None )

Represents a sync operation to be performed.

SyncPlan
class huggingface_hub.SyncPlan
<
source
>
( source: strdest: strtimestamp: stroperations: list = <factory> )

Represents a complete sync plan.

CommitInfo
class huggingface_hub.CommitInfo
<
source
>
( *argscommit_url: str**kwargs )

Parameters

commit_url (str) — Url where to find the commit.
commit_message (str) — The summary (first line) of the commit that has been created.
commit_description (str) — Description of the commit that has been created. Can be empty.
oid (str) — Commit hash id. Example: "91c54ad1727ee830252e457677f467be0bfd8a57".
pr_url (str, optional) — Url to the PR that has been created, if any. Populated when create_pr=True is passed.
pr_revision (str, optional) — Revision of the PR that has been created, if any. Populated when create_pr=True is passed. Example: "refs/pr/1".
pr_num (int, optional) — Number of the PR discussion that has been created, if any. Populated when create_pr=True is passed. Can be passed as discussion_num in get_discussion_details(). Example: 1.
repo_url (RepoUrl) — Repo URL of the commit containing info like repo_id, repo_type, etc.
Data structure containing information about a newly created commit.

Returned by any method that creates a commit on the Hub: create_commit(), upload_file(), upload_folder(), delete_file(), delete_folder(). It inherits from str for backward compatibility but using methods specific to str is deprecated.

DatasetInfo
class huggingface_hub.DatasetInfo
<
source
>
( **kwargs )

Expand 21 parameters
Parameters

id (str) — ID of dataset.
author (str) — Author of the dataset.
card_data (DatasetCardData, optional) — Dataset Card Metadata as a huggingface_hub.repocard_data.DatasetCardData object.
citation (str, optional) — Citation information for the dataset.
created_at (datetime, optional) — Date of creation of the repo on the Hub. Note that the lowest value is 2022-03-02T23:29:04.000Z, corresponding to the date when we began to store creation dates.
description (str, optional) — Description of the dataset.
disabled (bool, optional) — Is the repo disabled.
downloads (int) — Number of downloads of the dataset over the last 30 days.
downloads_all_time (int) — Cumulated number of downloads of the dataset since its creation.
gated (Literal["auto", "manual", False], optional) — Is the repo gated. If so, whether there is manual or automatic approval.
last_modified (datetime, optional) — Date of last commit to the repo.
likes (int) — Number of likes of the dataset.
main_size (int, optional) — Size in bytes of the main branch of the dataset.
paperswithcode_id (str, optional) — Papers with code ID of the dataset.
private (bool) — Is the repo private.
resource_group (dict, optional) — Resource group information for the dataset.
sha (str) — Repo SHA at this particular revision.
siblings (list[RepoSibling]) — List of huggingface_hub.hf_api.RepoSibling objects that constitute the dataset.
tags (list[str]) — List of tags of the dataset.
trending_score (int, optional) — Trending score of the dataset.
used_storage (int, optional) — Size in bytes of the dataset on the Hub.
Contains information about a dataset on the Hub. This object is returned by dataset_info() and list_datasets().

Most attributes of this class are optional. This is because the data returned by the Hub depends on the query made. In general, the more specific the query, the more information is returned. On the contrary, when listing datasets using list_datasets() only a subset of the attributes are returned.

DryRunFileInfo
class huggingface_hub.DryRunFileInfo
<
source
>
( commit_hash: strfile_size: intfilename: strlocal_path: stris_cached: boolwill_download: bool )

Parameters

commit_hash (str) — The commit_hash related to the file.
file_size (int) — Size of the file. In case of an LFS file, contains the size of the actual LFS file, not the pointer.
filename (str) — Name of the file in the repo.
is_cached (bool) — Whether the file is already cached locally.
will_download (bool) — Whether the file will be downloaded if hf_hub_download is called with dry_run=False. In practice, will_download is True if the file is not cached or if force_download=True.
Information returned when performing a dry run of a file download.

Returned by hf_hub_download() when dry_run=True.

GitRefInfo
class huggingface_hub.GitRefInfo
<
source
>
( name: strref: strtarget_commit: str )

Parameters

name (str) — Name of the reference (e.g. tag name or branch name).
ref (str) — Full git ref on the Hub (e.g. "refs/heads/main" or "refs/tags/v1.0").
target_commit (str) — OID of the target commit for the ref (e.g. "e7da7f221d5bf496a48136c0cd264e630fe9fcc8")
Contains information about a git reference for a repo on the Hub.

GitCommitInfo
class huggingface_hub.GitCommitInfo
<
source
>
( commit_id: strauthors: list[str]created_at: datetimetitle: strmessage: strformatted_title: str | Noneformatted_message: str | None )

Parameters

commit_id (str) — OID of the commit (e.g. "e7da7f221d5bf496a48136c0cd264e630fe9fcc8")
authors (list[str]) — List of authors of the commit.
created_at (datetime) — Datetime when the commit was created.
title (str) — Title of the commit. This is a free-text value entered by the authors.
message (str) — Description of the commit. This is a free-text value entered by the authors.
formatted_title (str) — Title of the commit formatted as HTML. Only returned if formatted=True is set.
formatted_message (str) — Description of the commit formatted as HTML. Only returned if formatted=True is set.
Contains information about a git commit for a repo on the Hub. Check out list_repo_commits() for more details.

GitRefs
class huggingface_hub.GitRefs
<
source
>
( branches: list[GitRefInfo]converts: list[GitRefInfo]tags: list[GitRefInfo]pull_requests: list[GitRefInfo] | None = None )

Parameters

branches (list[GitRefInfo]) — A list of GitRefInfo containing information about branches on the repo.
converts (list[GitRefInfo]) — A list of GitRefInfo containing information about “convert” refs on the repo. Converts are refs used (internally) to push preprocessed data in Dataset repos.
tags (list[GitRefInfo]) — A list of GitRefInfo containing information about tags on the repo.
pull_requests (list[GitRefInfo], optional) — A list of GitRefInfo containing information about pull requests on the repo. Only returned if include_prs=True is set.
Contains information about all git references for a repo on the Hub.

Object is returned by list_repo_refs().

InferenceProviderMapping
class huggingface_hub.hf_api.InferenceProviderMapping
<
source
>
( **kwargs )

KernelInfo
class huggingface_hub.KernelInfo
<
source
>
( **kwargs )

Parameters

id (str) — ID of the kernel repo.
author (str, optional) — Author of the kernel repo.
downloads (int, optional) — Number of downloads of the kernel repo over the last 30 days.
gated (Literal["auto", "manual", False], optional) — Is the repo gated. If so, whether there is manual or automatic approval.
last_modified (datetime, optional) — Date of last commit to the repo.
likes (int, optional) — Number of likes of the kernel repo.
private (bool, optional) — Is the repo private.
sha (str, optional) — Repo SHA at this particular revision.
Contains information about a kernel repo on the Hub. This object is returned by kernel_info().

LFSFileInfo
class huggingface_hub.hf_api.LFSFileInfo
<
source
>
( **kwargs )

Parameters

file_oid (str) — SHA-256 object ID of the file. This is the identifier to pass when permanently deleting the file.
filename (str) — Possible filename for the LFS object. See the note above for more information.
oid (str) — OID of the LFS object.
pushed_at (datetime) — Date the LFS object was pushed to the repo.
ref (str, optional) — Ref where the LFS object has been pushed (if any).
size (int) — Size of the LFS object.
Contains information about a file stored as LFS on a repo on the Hub.

Used in the context of listing and permanently deleting LFS files from a repo to free-up space. See list_lfs_files() and permanently_delete_lfs_files() for more details.

Git LFS files are tracked using SHA-256 object IDs, rather than file paths, to optimize performance This approach is necessary because a single object can be referenced by multiple paths across different commits, making it impractical to search and resolve these connections. Check out our documentation to learn how to know which filename(s) is(are) associated with each SHA.

Example:

Copied
from huggingface_hub import HfApi
api = HfApi()
lfs_files = api.list_lfs_files("username/my-cool-repo")

# Filter files files to delete based on a combination of `filename`, `pushed_at`, `ref` or `size`.
# e.g. select only LFS files in the "checkpoints" folder
lfs_files_to_delete = (lfs_file for lfs_file in lfs_files if lfs_file.filename.startswith("checkpoints/"))

# Permanently delete LFS files
api.permanently_delete_lfs_files("username/my-cool-repo", lfs_files_to_delete)
ModelInfo
class huggingface_hub.ModelInfo
<
source
>
( **kwargs )

Expand 33 parameters
Parameters

id (str) — ID of model.
author (str, optional) — Author of the model.
base_models (list[str], optional) — List of base models this model is derived from.
card_data (ModelCardData, optional) — Model Card Metadata as a huggingface_hub.repocard_data.ModelCardData object.
children_model_count (int, optional) — Number of children models derived from this model.
config (dict, optional) — Model configuration.
created_at (datetime, optional) — Date of creation of the repo on the Hub. Note that the lowest value is 2022-03-02T23:29:04.000Z, corresponding to the date when we began to store creation dates.
disabled (bool, optional) — Is the repo disabled.
downloads (int) — Number of downloads of the model over the last 30 days.
downloads_all_time (int) — Cumulated number of downloads of the model since its creation.
eval_results (list[EvalResultEntry], optional) — Model’s evaluation results.
gated (Literal["auto", "manual", False], optional) — Is the repo gated. If so, whether there is manual or automatic approval.
gguf (dict, optional) — GGUF information of the model.
inference (Literal["warm"], optional) — Status of the model on Inference Providers. Warm if the model is served by at least one provider.
inference_provider_mapping (list[InferenceProviderMapping], optional) — A list of InferenceProviderMapping ordered after the user’s provider order.
last_modified (datetime, optional) — Date of last commit to the repo.
library_name (str, optional) — Library associated with the model.
likes (int) — Number of likes of the model.
mask_token (str, optional) — Mask token used by the model.
model_index (dict, optional) — Model index for evaluation.
pipeline_tag (str, optional) — Pipeline tag associated with the model.
private (bool) — Is the repo private.
resource_group (dict, optional) — Resource group information for the model.
safetensors (SafeTensorsInfo, optional) — Model’s safetensors information.
security_repo_status (dict, optional) — Model’s security scan status.
sha (str, optional) — Repo SHA at this particular revision.
siblings (list[RepoSibling]) — List of huggingface_hub.hf_api.RepoSibling objects that constitute the model.
spaces (list[str], optional) — List of spaces using the model.
tags (list[str]) — List of tags of the model. Compared to card_data.tags, contains extra tags computed by the Hub (e.g. supported libraries, model’s arXiv).
transformers_info (TransformersInfo, optional) — Transformers-specific info (auto class, processor, etc.) associated with the model.
trending_score (int, optional) — Trending score of the model.
used_storage (int, optional) — Size in bytes of the model on the Hub.
widget_data (Any, optional) — Widget data associated with the model.
Contains information about a model on the Hub. This object is returned by model_info() and list_models().

Most attributes of this class are optional. This is because the data returned by the Hub depends on the query made. In general, the more specific the query, the more information is returned. On the contrary, when listing models using list_models() only a subset of the attributes are returned.

RepoSibling
class huggingface_hub.hf_api.RepoSibling
<
source
>
( rfilename: strsize: int | None = Noneblob_id: str | None = Nonelfs: BlobLfsInfo | None = None )

Parameters

rfilename (str) — file name, relative to the repo root.
size (int, optional) — The file’s size, in bytes. This attribute is defined when files_metadata argument of repo_info() is set to True. It’s None otherwise.
blob_id (str, optional) — The file’s git OID. This attribute is defined when files_metadata argument of repo_info() is set to True. It’s None otherwise.
lfs (BlobLfsInfo, optional) — The file’s LFS metadata. This attribute is defined whenfiles_metadata argument of repo_info() is set to True and the file is stored with Git LFS. It’s None otherwise.
Contains basic information about a repo file inside a repo on the Hub.

All attributes of this class are optional except rfilename. This is because only the file names are returned when listing repositories on the Hub (with list_models(), list_datasets() or list_spaces()). If you need more information like file size, blob id or lfs details, you must request them specifically from one repo at a time (using model_info(), dataset_info() or space_info()) as it adds more constraints on the backend server to retrieve these.

RepoFile
class huggingface_hub.RepoFile
<
source
>
( **kwargs )

Parameters

path (str) — file path relative to the repo root.
size (int) — The file’s size, in bytes.
blob_id (str) — The file’s git OID.
lfs (BlobLfsInfo, optional) — The file’s LFS metadata.
xet_hash (str, optional) — The file’s Xet hash.
last_commit (LastCommitInfo, optional) — The file’s last commit metadata. Only defined if list_repo_tree() and get_paths_info() are called with expand=True.
security (BlobSecurityInfo, optional) — The file’s security scan metadata. Only defined if list_repo_tree() and get_paths_info() are called with expand=True.
Contains information about a file on the Hub.

RepoUrl
class huggingface_hub.RepoUrl
<
source
>
( url: Anyendpoint: str | None = None )

Parameters

url (Any) — String value of the repo url.
endpoint (str, optional) — Endpoint of the Hub. Defaults to https://huggingface.co.
Raises

HfUriError

HfUriError — If the URL cannot be parsed (e.g. canonical single-segment repo, or unknown repo_type).

Subclass of str describing a repo URL on the Hub.

RepoUrl is returned by HfApi.create_repo. It inherits from str for backward compatibility. At initialization, the URL is parsed to populate properties:

endpoint (str)
namespace (str)
repo_name (str)
repo_id (str)
repo_type (Literal["model", "dataset", "space"])
url (str)
Example:

Copied
RepoUrl('https://huggingface.co/openai-community/gpt2')
RepoUrl('https://huggingface.co/openai-community/gpt2', endpoint='https://huggingface.co', repo_type='model', repo_id='openai-community/gpt2')

RepoUrl('https://hub-ci.huggingface.co/datasets/dummy_user/dummy_dataset', endpoint='https://hub-ci.huggingface.co')
RepoUrl('https://hub-ci.huggingface.co/datasets/dummy_user/dummy_dataset', endpoint='https://hub-ci.huggingface.co', repo_type='dataset', repo_id='dummy_user/dummy_dataset')

RepoUrl('hf://datasets/my-user/my-dataset')
RepoUrl('hf://datasets/my-user/my-dataset', endpoint='https://huggingface.co', repo_type='dataset', repo_id='user/dataset')

HfApi.create_repo("dummy_model")
RepoUrl('https://huggingface.co/Wauplin/dummy_model', endpoint='https://huggingface.co', repo_type='model', repo_id='Wauplin/dummy_model')
SafetensorsRepoMetadata
class huggingface_hub.utils.SafetensorsRepoMetadata
<
source
>
( metadata: dict | Nonesharded: boolweight_map: dictfiles_metadata: dict )

Parameters

metadata (dict, optional) — The metadata contained in the ‘model.safetensors.index.json’ file, if it exists. Only populated for sharded models.
sharded (bool) — Whether the repo contains a sharded model or not.
weight_map (dict[str, str]) — A map of all weights. Keys are tensor names and values are filenames of the files containing the tensors.
files_metadata (dict[str, SafetensorsFileMetadata]) — A map of all files metadata. Keys are filenames and values are the metadata of the corresponding file, as a SafetensorsFileMetadata object.
parameter_count (dict[str, int]) — A map of the number of parameters per data type. Keys are data types and values are the number of parameters of that data type.
Metadata for a Safetensors repo.

A repo is considered to be a Safetensors repo if it contains either a ‘model.safetensors’ weight file (non-shared model) or a ‘model.safetensors.index.json’ index file (sharded model) at its root.

This class is returned by get_safetensors_metadata().

For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

SafetensorsFileMetadata
class huggingface_hub.utils.SafetensorsFileMetadata
<
source
>
( metadata: dicttensors: dict )

Parameters

metadata (dict) — The metadata contained in the file.
tensors (dict[str, TensorInfo]) — A map of all tensors. Keys are tensor names and values are information about the corresponding tensor, as a TensorInfo object.
parameter_count (dict[str, int]) — A map of the number of parameters per data type. Keys are data types and values are the number of parameters of that data type.
Metadata for a Safetensors file hosted on the Hub.

This class is returned by parse_safetensors_file_metadata().

For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

SpaceInfo
class huggingface_hub.SpaceInfo
<
source
>
( **kwargs )

Expand 21 parameters
Parameters

id (str) — ID of the Space.
author (str, optional) — Author of the Space.
card_data (SpaceCardData, optional) — Space Card Metadata as a huggingface_hub.repocard_data.SpaceCardData object.
created_at (datetime, optional) — Date of creation of the repo on the Hub. Note that the lowest value is 2022-03-02T23:29:04.000Z, corresponding to the date when we began to store creation dates.
datasets (list[str], optional) — List of datasets used by the Space.
disabled (bool, optional) — Is the Space disabled.
gated (Literal["auto", "manual", False], optional) — Is the repo gated. If so, whether there is manual or automatic approval.
host (str, optional) — Host URL of the Space.
last_modified (datetime, optional) — Date of last commit to the repo.
likes (int) — Number of likes of the Space.
models (list[str], optional) — List of models used by the Space.
private (bool) — Is the repo private.
resource_group (dict, optional) — Resource group information for the Space.
runtime (SpaceRuntime, optional) — Space runtime information as a huggingface_hub.hf_api.SpaceRuntime object.
sdk (str, optional) — SDK used by the Space.
sha (str, optional) — Repo SHA at this particular revision.
siblings (list[RepoSibling]) — List of huggingface_hub.hf_api.RepoSibling objects that constitute the Space.
subdomain (str, optional) — Subdomain of the Space.
tags (list[str]) — List of tags of the Space.
trending_score (int, optional) — Trending score of the Space.
used_storage (int, optional) — Size in bytes of the Space on the Hub.
Contains information about a Space on the Hub. This object is returned by space_info() and list_spaces().

Most attributes of this class are optional. This is because the data returned by the Hub depends on the query made. In general, the more specific the query, the more information is returned. On the contrary, when listing spaces using list_spaces() only a subset of the attributes are returned.

SpaceSearchResult
class huggingface_hub.SpaceSearchResult
<
source
>
( data: dict )

Parameters

id (str) — ID of the Space (e.g. "username/repo-name").
author (str) — Author of the Space.
title (str) — Display title of the Space.
emoji (str or None) — Emoji icon of the Space.
sdk (str or None) — SDK used by the Space (e.g. "gradio", "docker", "static").
likes (int) — Number of likes.
private (bool) — Whether the Space is private.
tags (list[str] or None) — List of tags.
runtime (SpaceRuntime or None) — Runtime information (stage, hardware, etc.).
ai_short_description (str or None) — AI-generated short description.
ai_category (str or None) — AI-generated category (e.g. "Image Generation").
semantic_relevancy_score (float or None) — Semantic relevancy score (0-1) relative to the search query.
trending_score (int or None) — Trending score.
A single result from the Spaces semantic search API.

Returned by HfApi.search_spaces().

TensorInfo
class huggingface_hub.utils.TensorInfo
<
source
>
( dtype: typing.Literal['F64', 'F32', 'F16', 'BF16', 'I64', 'I32', 'I16', 'I8', 'U8', 'BOOL']shape: listdata_offsets: tuple )

Parameters

dtype (str) — The data type of the tensor (“F64”, “F32”, “F16”, “BF16”, “I64”, “I32”, “I16”, “I8”, “U8”, “BOOL”).
shape (list[int]) — The shape of the tensor.
data_offsets (tuple[int, int]) — The offsets of the data in the file as a tuple [BEGIN, END].
parameter_count (int) — The number of parameters in the tensor.
Information about a tensor.

For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

User
class huggingface_hub.User
<
source
>
( **kwargs )

Expand 16 parameters
Parameters

username (str) — Name of the user on the Hub (unique).
fullname (str) — User’s full name.
avatar_url (str) — URL of the user’s avatar.
details (str, optional) — User’s details.
is_following (bool, optional) — Whether the authenticated user is following this user.
is_pro (bool, optional) — Whether the user is a pro user.
num_models (int, optional) — Number of models created by the user.
num_datasets (int, optional) — Number of datasets created by the user.
num_spaces (int, optional) — Number of spaces created by the user.
num_discussions (int, optional) — Number of discussions initiated by the user.
num_papers (int, optional) — Number of papers authored by the user.
num_upvotes (int, optional) — Number of upvotes received by the user.
num_likes (int, optional) — Number of likes given by the user.
num_following (int, optional) — Number of users this user is following.
num_followers (int, optional) — Number of users following this user.
orgs (list of Organization) — List of organizations the user is part of.
Contains information about a user on the Hub.

UserLikes
class huggingface_hub.UserLikes
<
source
>
( user: strtotal: intdatasets: list[str]kernels: list[str]models: list[str]spaces: list[str] )

Parameters

user (str) — Name of the user for which we fetched the likes.
total (int) — Total number of likes.
datasets (list[str]) — List of datasets liked by the user (as repo_ids).
kernels (list[str]) — List of kernels liked by the user (as repo_ids).
models (list[str]) — List of models liked by the user (as repo_ids).
spaces (list[str]) — List of spaces liked by the user (as repo_ids).
Contains information about a user likes on the Hub.

WebhookInfo
class huggingface_hub.WebhookInfo
<
source
>
( id: strurl: str | Nonejob: JobSpec | Nonewatched: list[WebhookWatchedItem]domains: list[constants.WEBHOOK_DOMAIN_T]secret: str | Nonedisabled: bool )

Parameters

id (str) — ID of the webhook.
url (str, optional) — URL of the webhook.
job (JobSpec, optional) — Specifications of the Job to trigger.
watched (list[WebhookWatchedItem]) — List of items watched by the webhook, see WebhookWatchedItem.
domains (list[WEBHOOK_DOMAIN_T]) — List of domains the webhook is watching. Can be one of ["repo", "discussions"].
secret (str, optional) — Secret of the webhook.
disabled (bool) — Whether the webhook is disabled or not.
Data structure containing information about a webhook.

One of url or job is specified, but not both.

WebhookWatchedItem
class huggingface_hub.WebhookWatchedItem
<
source
>
( type: Literal['dataset', 'model', 'org', 'space', 'user']name: str )

Parameters

type (Literal["dataset", "model", "org", "space", "user"]) — Type of the item to be watched. Can be one of ["dataset", "model", "org", "space", "user"].
name (str) — Name of the item to be watched. Can be the username, organization name, model name, dataset name or space name.
Data structure containing information about the items watched by a webhook.

CommitOperation
Below are the supported values for CommitOperation():

class huggingface_hub.CommitOperationAdd
<
source
>
( path_in_repo: strpath_or_fileobj: str | pathlib.Path | bytes | typing.BinaryIO )

Parameters

path_in_repo (str) — Relative filepath in the repo, for example: "checkpoints/1fec34a/weights.bin"
path_or_fileobj (str, Path, bytes, or BinaryIO) — Either:
a path to a local file (as str or pathlib.Path) to upload
a buffer of bytes (bytes) holding the content of the file to upload
a “file object” (subclass of io.BufferedIOBase), typically obtained with open(path, "rb"). It must support seek() and tell() methods.
Raises

ValueError

ValueError — If path_or_fileobj is not one of str, Path, bytes or io.BufferedIOBase.
ValueError — If path_or_fileobj is a str or Path but not a path to an existing file.
ValueError — If path_or_fileobj is a io.BufferedIOBase but it doesn’t support both seek() and tell().

Data structure holding necessary info to upload a file to a repository on the Hub.

as_file
<
source
>
( with_tqdm: bool = False )

Parameters

with_tqdm (bool, optional, defaults to False) — If True, iterating over the file object will display a progress bar. Only works if the file-like object is a path to a file. Pure bytes and buffers are not supported.
A context manager that yields a file-like object allowing to read the underlying data behind path_or_fileobj.

Example:

Copied
operation = CommitOperationAdd(
       path_in_repo="remote/dir/weights.h5",
       path_or_fileobj="./local/weights.h5",
)
CommitOperationAdd(path_in_repo='remote/dir/weights.h5', path_or_fileobj='./local/weights.h5')

with operation.as_file() as file:
    content = file.read()

with operation.as_file(with_tqdm=True) as file:
    while True:
        data = file.read(1024)
        if not data:
             break
config.json: 100%|█████████████████████████| 8.19k/8.19k [00:02<00:00, 3.72kB/s]

with operation.as_file(with_tqdm=True) as file:
    httpx.put(..., data=file)
config.json: 100%|█████████████████████████| 8.19k/8.19k [00:02<00:00, 3.72kB/s]
b64content
<
source
>
( )

The base64-encoded content of path_or_fileobj

Returns: bytes

class huggingface_hub.CommitOperationDelete
<
source
>
( path_in_repo: stris_folder: typing.Union[bool, typing.Literal['auto']] = 'auto' )

Parameters

path_in_repo (str) — Relative filepath in the repo, for example: "checkpoints/1fec34a/weights.bin" for a file or "checkpoints/1fec34a/" for a folder.
is_folder (bool or Literal["auto"], optional) — Whether the Delete Operation applies to a folder or not. If “auto”, the path type (file or folder) is guessed automatically by looking if path ends with a ”/” (folder) or not (file). To explicitly set the path type, you can set is_folder=True or is_folder=False.
Data structure holding necessary info to delete a file or a folder from a repository on the Hub.

class huggingface_hub.CommitOperationCopy
<
source
>
( src_path_in_repo: strpath_in_repo: strsrc_revision: str | None = Nonesrc_repo_id: str | None = Nonesrc_repo_type: str | None = None_src_oid: str | None = None_dest_oid: str | None = None_is_duplicated: bool = False )

Parameters

src_path_in_repo (str) — Relative filepath in the repo of the file to be copied, e.g. "checkpoints/1fec34a/weights.bin".
path_in_repo (str) — Relative filepath in the repo where to copy the file, e.g. "checkpoints/1fec34a/weights_copy.bin".
src_revision (str, optional) — The git revision of the file to be copied. Can be any valid git revision. Default to the target commit revision.
src_repo_id (str, optional) — The source repository to copy from (e.g. "username/source-model"). Default to the destination repository (intra-repo copy).
src_repo_type (str, optional) — The type of the source repository ("model", "dataset" or "space"). Required when src_repo_id is set.
Data structure holding necessary info to copy a file in a repository on the Hub.

Both LFS files and regular files are supported. LFS files are copied server-side while regular files are downloaded and re-uploaded as part of the commit.

Cross-repository copies are supported by setting src_repo_id and src_repo_type. For cross-repo LFS copies, the LFS objects are duplicated to the destination repository before the commit is created. This is handled automatically by create_commit(). Note that cross-repository copies only work within the same storage region; copying across regions is not supported.

Note: you can combine a CommitOperationCopy and a CommitOperationDelete to rename an LFS file on the Hub.

CommitScheduler
class huggingface_hub.CommitScheduler
<
source
>
( repo_id: strfolder_path: str | pathlib.Pathevery: int | float = 5path_in_repo: str | None = Nonerepo_type: str | None = Nonerevision: str | None = Noneprivate: bool | None = Nonetoken: str | None = Noneallow_patterns: list[str] | str | None = Noneignore_patterns: list[str] | str | None = Nonesquash_history: bool = Falsehf_api: typing.Optional[ForwardRef('HfApi')] = None )

Parameters

repo_id (str) — The id of the repo to commit to.
folder_path (str or Path) — Path to the local folder to upload regularly.
every (int or float, optional) — The number of minutes between each commit. Defaults to 5 minutes.
path_in_repo (str, optional) — Relative path of the directory in the repo, for example: "checkpoints/". Defaults to the root folder of the repository.
repo_type (str, optional) — The type of the repo to commit to. Defaults to model.
revision (str, optional) — The revision of the repo to commit to. Defaults to main.
private (bool, optional) — Whether to make the repo private. If None (default), the repo will be public unless the organization’s default is private. This value is ignored if the repo already exists.
token (str, optional) — The token to use to commit to the repo. Defaults to the token saved on the machine.
allow_patterns (list[str] or str, optional) — If provided, only files matching at least one pattern are uploaded.
ignore_patterns (list[str] or str, optional) — If provided, files matching any of the patterns are not uploaded.
squash_history (bool, optional) — Whether to squash the history of the repo after each commit. Defaults to False. Squashing commits is useful to avoid degraded performances on the repo when it grows too large.
hf_api (HfApi, optional) — The HfApi client to use to commit to the Hub. Can be set with custom settings (user agent, token,…).
Scheduler to upload a local folder to the Hub at regular intervals (e.g. push to hub every 5 minutes).

The recommended way to use the scheduler is to use it as a context manager. This ensures that the scheduler is properly stopped and the last commit is triggered when the script ends. The scheduler can also be stopped manually with the stop method. Checkout the upload guide to learn more about how to use it.

Example:

Copied
from pathlib import Path
from huggingface_hub import CommitScheduler

# Scheduler uploads every 10 minutes
csv_path = Path("watched_folder/data.csv")
CommitScheduler(repo_id="test_scheduler", repo_type="dataset", folder_path=csv_path.parent, every=10)

with csv_path.open("a") as f:
    f.write("first line")

# Some time later (...)
with csv_path.open("a") as f:
    f.write("second line")
Example using a context manager:

Copied
from pathlib import Path
from huggingface_hub import CommitScheduler

with CommitScheduler(repo_id="test_scheduler", repo_type="dataset", folder_path="watched_folder", every=10) as scheduler:
    csv_path = Path("watched_folder/data.csv")
    with csv_path.open("a") as f:
        f.write("first line")
    (...)
    with csv_path.open("a") as f:
        f.write("second line")

# Scheduler is now stopped and last commit have been triggered
push_to_hub
<
source
>
( )

Push folder to the Hub and return the commit info.

This method is not meant to be called directly. It is run in the background by the scheduler, respecting a queue mechanism to avoid concurrent commits. Making a direct call to the method might lead to concurrency issues.

The default behavior of push_to_hub is to assume an append-only folder. It lists all files in the folder and uploads only changed files. If no changes are found, the method returns without committing anything. If you want to change this behavior, you can inherit from CommitScheduler and override this method. This can be useful for example to compress data together in a single file before committing. For more details and examples, check out our integration guide.

stop
<
source
>
( )

Stop the scheduler.

A stopped scheduler cannot be restarted. Mostly for tests purposes.

trigger
<
source
>
( )

Trigger a push_to_hub and return a future.

This method is automatically called every every minutes. You can also call it manually to trigger a commit immediately, without waiting for the next scheduled commit.

Update on GitHub