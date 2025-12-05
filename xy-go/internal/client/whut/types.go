package whut

import "time"

const URL = "https://infra.ai-augmented.com/"

type clientId string

const whut clientId = "xy_client_whut"
const ccnu clientId = "xy_client_ccnu"
const ksu clientId = "xy_client_ksu"

func (client clientId) String() string {
	return string(client)
}

type schools struct {
	School []school `json:"schools"`
}

type baseResp[T any] struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
	Data    T      `json:"data"`
}

type school struct {
	Id          string `json:"id"`
	Code        string `json:"code"`
	Name        string `json:"name"`
	DisplayName string `json:"displayName"`
}

type schoolsResp baseResp[schools]

type loginReq struct {
	Account           string `json:"account"`
	Password          string `json:"password"`
	SchoolId          string `json:"schoolId"`
	ClientId          string `json:"clientId"`
	State             string `json:"state"` // 随机6位字符串
	RedirectUri       string `json:"redirectUri"`
	WeekNoLoginStatus bool   `json:"weekNoLoginStatus"`
}

type loginInfo struct {
	Valid          bool `json:"valid"`
	IsLoginByPhone bool `json:"isLoginByPhone"`
}

type loginResp baseResp[loginInfo]
type account struct {
	Id        string `json:"id"`
	LoginName string `json:"loginName"`
	Status    string `json:"status"`
	School    struct {
		Id          string `json:"id"`
		Code        string `json:"code"`
		Name        string `json:"name"`
		DisplayName string `json:"displayName"`
		InstanceId  string `json:"instanceId"`
	} `json:"school"`
	IsInCurrentInstance bool `json:"isInCurrentInstance"`
}

type accountWrapper struct {
	Accounts []account `json:"accounts"`
}

type listAccountsResp baseResp[accountWrapper]

type listCourseResp baseResp[[]course]

type course struct {
	Id                   string        `json:"id"`
	SiteId               string        `json:"site_id"`
	VisitNumber          int           `json:"visit_number"`
	CustomInfo           interface{}   `json:"custom_info"`
	IsResourceAutoPublic bool          `json:"is_resource_auto_public"`
	SiteName             string        `json:"site_name"`
	Key                  int           `json:"key"`
	JoinType             int           `json:"join_type"`
	Creator              string        `json:"creator"`
	Status               int           `json:"status"`
	Lock                 int           `json:"lock"`
	CoverImg             string        `json:"cover_img"`
	Description          string        `json:"description"`
	Filed                int           `json:"filed"`
	Statistics           int           `json:"statistics"`
	CreatedAt            string        `json:"created_at"`
	UpdatedAt            string        `json:"updated_at"`
	StartTime            string        `json:"start_time"`
	EndTime              string        `json:"end_time"`
	SchoolId             string        `json:"school_id"`
	DomainCode           string        `json:"domain_code"`
	CourseType           string        `json:"course_type"`
	CourseProperty       string        `json:"course_property"`
	DepartmentCode       string        `json:"department_code"`
	CourseCode           string        `json:"course_code"`
	TermCode             string        `json:"term_code"`
	PublicType           string        `json:"public_type"`
	OriginType           string        `json:"origin_type"`
	IdentityFlag         int           `json:"identity_flag"`
	SchoolName           string        `json:"school_name"`
	TermName             string        `json:"term_name"`
	DepartmentName       string        `json:"department_name"`
	DomainName           string        `json:"domain_name"`
	PublicTypeName       string        `json:"public_type_name"`
	OriginTypeName       string        `json:"origin_type_name"`
	TeacherNames         string        `json:"teacher_names"`
	MemberCount          int           `json:"member_count"`
	CreatedAt1           time.Time     `json:"createdAt"`
	Role                 int           `json:"role"`
	Teachers             []interface{} `json:"teachers"`
	Name                 string        `json:"name"`
}

type tasks struct {
	TaskId                string        `json:"task_id"`
	GroupId               string        `json:"group_id"`
	NodeId                string        `json:"node_id"`
	CreatorId             string        `json:"creator_id"`
	AssignToType          int           `json:"assign_to_type"`
	TaskType              int           `json:"task_type"`
	IsClassTask           bool          `json:"is_class_task"`
	StartTime             time.Time     `json:"start_time"`
	EndTime               time.Time     `json:"end_time"`
	FinishType            int           `json:"finish_type"`
	PaperPublishId        string        `json:"paper_publish_id"`
	IsAllowAfterSubmitted bool          `json:"is_allow_after_submitted"`
	CreatedAt             time.Time     `json:"created_at"`
	WatchMinMinutes       int           `json:"watch_min_minutes"`
	AssignId              string        `json:"assign_id"`
	AssignToId            string        `json:"assign_to_id"`
	Finish                int           `json:"finish"`
	FinishTime            time.Time     `json:"finish_time"`
	Id                    string        `json:"id"`
	ParentId              string        `json:"parent_id"`
	QuoteId               string        `json:"quote_id"`
	Subgroups             []interface{} `json:"subgroups"`
}

type queryTasksResp baseResp[struct {
	TeacherTasks []tasks `json:"teacher_tasks"`
	StudentTasks []tasks `json:"student_tasks"`
}]
